# Jarvis Prestidge & Kanita Dogra
# Decription:   tbc

# Including imports

import collections
import platform
import os
import time
import csv

from datetime import timedelta, datetime

from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

verbose = False

base_url = "https://www.whoscored.com"

print "\nTaran's whoscored.com webscraping script.\n"

# PhantomJS files have different extensions
# under different operating systems
if platform.system() == 'Windows':
    print "Windows OS detected"
    phantomjs_path = './phantomjs.exe'
else:
    print "UNIX derived OS deteceted"
    phantomjs_path = './phantomjs'

if os.path.isfile('./phantomjs.exe'):
    print "Found phantomjs headless webkit"
else:
    print "Can not find phantomjs in current directory"
    print("Exiting...")
    raise SystemExit

print "\n================================================================\n"

print "Loading available leagues...\n"

browser = webdriver.PhantomJS(phantomjs_path)
# The home url of the english leagues
browser.get(base_url + "/Regions/252/Tournaments/2")
time.sleep(10)

# Parsing the content using the default python html parser
soup = BeautifulSoup(browser.page_source, 'html.parser')

# Removing script tag for visiblitly
[s.extract() for s in soup('script')]

# Getting list of 'select' combo box tags
league_soup = soup.find('select', {'id': 'tournaments'})('option')

# Creating a tuple to hold seasons and respective urls
League = collections.namedtuple('League', 'name url')

# Creating a list to hold said tuple seasons
leagues = list()

# Adding each season and url to a tuple and then appending to list
for option in league_soup:
    leagues.append(League(name=option.get_text(), url=option.get('value')))

print "League\n"

league_url = ""
league_str = ""

while True:
    count = 0
    for league in leagues:
        count += 1
        print '{:3}: {:20}'.format(str(count), league.name)
    q1_input = raw_input("\nPlease select a league: ")
    if q1_input.isdigit() and \
       (int(q1_input) > 0 and int(q1_input) <= len(leagues)):
        # Creating the league url global variable
        league_url = base_url + leagues[int(q1_input) - 1].url
        league_str = leagues[int(q1_input) - 1].name
        print "\nAccepted."
        # Exiting the loop
        break
    else:
        print("\nPlease enter a valid league number only.\n")

print "\n================================================================\n"

print "Loading available seasons based on league selection...\n"

browser = webdriver.PhantomJS(phantomjs_path)
browser.get(league_url)
time.sleep(10)

# Parsing the content using the default python html parser
soup = BeautifulSoup(browser.page_source, 'html.parser')

# Removing script tag for visiblitly
[s.extract() for s in soup('script')]

# Getting list of 'select' combo box tags
season_soup = soup.find('select', {'id': 'seasons'})('option')

# Creating a tuple to hold seasons and respective urls
Season = collections.namedtuple('Season', 'name url')

# Creating a list to hold said tuple seasons
seasons = list()

# Adding each season and url to a tuple and then appending to list
for option in season_soup:
    seasons.append(Season(name=option.get_text(), url=option.get('value')))

print "Season\n"

season_url = ""
season_str = ""

while True:
    count = 0
    for season in seasons:
        count += 1
        print '{:3}: {:20}'.format(str(count), season.name)
    q2_input = raw_input("\nPlease select a season: ")
    if q2_input.isdigit() and \
       (int(q2_input) > 0 and int(q2_input) <= len(seasons)):
        # Creating season url global variable
        season_url = base_url + seasons[int(q2_input) - 1].url
        season_str = seasons[int(q2_input) - 1].name
        print "\nAccepted."
        # Exiting the loop
        break
    else:
        print("\nPlease enter a valid season number only.\n")

print("\n================================================================\n")

while True:
    q3_input = raw_input("Would you like to print scraped data to the "
                         "console in a human \nreadable format? (Y/n) ")
    if q3_input.lower() == 'y' or q3_input == "":
        print "\nAccepted."
        verbose = True
        break
    elif q3_input.lower() == 'n':
        break
    else:
        print("\nPlease enter either <y> or <n> only.\n")

print("\n================================================================\n")

print "Fetching data...\n"

# Loading page based on chosen season
browser.get(season_url)
time.sleep(10)

# Parsing the content using the default python html parser
soup = BeautifulSoup(browser.page_source, 'html.parser')

# Removing script tag for visiblitly
[s.extract() for s in soup('script')]

# Getting fixture page url
fixture_url = base_url + \
    soup.find('div', {'id': 'sub-navigation'})('a')[1].get('href')

browser.get(fixture_url)
time.sleep(10)

# Parsing the content using the default python html parser
soup = BeautifulSoup(browser.page_source, 'html.parser')

print "Success!"

print("\n================================================================\n")

print "Travelling back through season months...\n"

while True:

    # Test if no more months to back track through
    if soup.find('a',
                 {'class': 'previous button ui-state-default rc-l is-disabled'}) is None:
        # Get handle to "previous" button
        browser.save_screenshot('screenshot.png')
        el = browser.find_element_by_xpath(
            '//a[@class="previous button ui-state-default rc-l is-default"]')
    else:
        break

    # Perform click
    webdriver.ActionChains(browser).move_to_element(el).click(el).perform()

    # Attempt to give browser enough time to load the page
    delay = 10
    try:
        WebDriverWait(browser, delay).until(
            EC.presence_of_element_located((
                By.ID, 'tournament-fixture-wrapper')))
    except TimeoutException:
        print "Loading took too much time!"
    except Exception:
        print "Unknown exception occurred!"

    time.sleep(10)

    # Parsing the content using the default python html parser
    soup = BeautifulSoup(browser.page_source, 'html.parser')

    # Print month
    print soup.find(
        'a', {'id': 'date-config-toggle-button'})('span')[0].get_text() + "\n"

print "Successfully reached start of " + season_str + " season."

print("\n================================================================\n")

# Removing script tag for visiblitly"
[s.extract() for s in soup('script')]

# =============
# Scraping
# =============

print "Fetching fixture meta data by month\n"


def strtodate(date_str):
    # Turns a string into a date object
    date = datetime.strptime(str(date_str), "%A, %b %d %Y")
    return date

# Getting the start of season date
initial_date_str = soup.find('th').get_text()
initial_date = strtodate(initial_date_str)
print "First match of season: " + initial_date_str + "\n"


def week(game_date):
    # Defining function to calculate the different weeks
    monday1 = (initial_date - timedelta(days=initial_date.weekday()))
    monday2 = (game_date - timedelta(days=game_date.weekday()))
    return (monday2 - monday1).days / 7

break_check = False
week_counter = 0
date_counter = initial_date_str

# The one list to hold them all!
fixtures = list()

# Creating named tuple object to hold pertinent data
Fixture = collections.namedtuple(
    'Fixture', 'date week kickoff home away url')

# Looping through each month
while True:
    print "Current month: " + soup.find(
        'a', {'id': 'date-config-toggle-button'})('span')[0].get_text()

    # Gathering list of all fixture rows
    rows = soup.find('table', id='tournament-fixture')('tr')

    fixture_counter = 0

    for row in rows:
        # For each row we either append to 'Fixtures' or record date
        if row.find('th') is None:
            fixture_counter += 1

            # Test if fixture has been played yet
            if row.find('a', {'class': 'match-link match-report rc'}) is None:
                break_check = True
                break

            # Fixture - we collect pertinent info
            fixtures.append(Fixture(
                date=date_counter,
                week=week_counter,
                kickoff=row.find('td', {'class': 'time'}).get_text(),
                home=row('a', {'class': 'team-link '})[0].get_text(),
                away=row('a', {'class': 'team-link '})[1].get_text(),
                url=row.find(
                    'a', {'class': 'match-link match-report rc'}).get('href')
            ))
            # somehow append this tuple to list
            continue
        else:
            # Date header - we log the current week & date
            week_counter = week(strtodate(row.get_text()))
            date_counter = row.get_text()
            continue

    print "Fixtures captured: " + str(fixture_counter)

    # Check if this was the last page
    if break_check is True:
        # If true then quit the loop
        break

    # Get handle to "next" button
    el = browser.find_element_by_xpath(
        '//a[@class="next button ui-state-default rc-r is-default"]')

    # Perform click
    webdriver.ActionChains(browser).move_to_element(el).click(el).perform()

    # Attempting to give the browser enough time to load the page
    delay = 10
    try:
        WebDriverWait(browser, delay).until(
            EC.presence_of_element_located((
                By.ID, 'tournament-fixture-wrapper')))
    except TimeoutException:
        print "Loading took too much time!"
    except Exception:
        print "Unknown exception occurred!"

    time.sleep(10)

    # Parsing the content using the default python html parser
    soup = BeautifulSoup(browser.page_source, 'html.parser')

    if soup.find('a',
       {'class': 'next button ui-state-default rc-r is-disabled'}) is not None:
        break_check = True

print "\nFinished scraping fixture meta data!\n"

print "====================================\n"

for num, match in enumerate(fixtures):
    print "Match #" + str(num)
    print "date: " + match.date
    print "week: " + str(match.week)
    print "kickoff: " + match.kickoff
    print "home: " + match.home
    print "away: " + match.away
    print "url: " + match.url
    print "\n====================================\n"


print "Commencing individual fixure data scraping...\n"
# Loop through the list of fixtures scraping and writing to csv as we go.

for match in fixtures:

    # Building url to scrape
    url = base_url + \
        match.url[:-12] + \
        "/Live/England-Premier-League-2015-2016-" + \
        str(match.home).replace(' ', '-') + \
        "-" + \
        str(match.away).replace(' ', '-')

    print url

    browser.get(url)
    time.sleep(5)

    el = browser.find_element_by_xpath('//a[@href="#chalkboard"]')
    webdriver.ActionChains(browser).move_to_element(el).click(el).perform()

    # Attempting to give the browser enough time to load the page
    delay = 10
    try:
        WebDriverWait(browser, delay).until(
            EC.presence_of_element_located((By.ID, 'chalkboard-timeline')))
    except TimeoutException:
        print "Loading took too much time!"
    except Exception:
        print "Unknown exception occureed!"

    time.sleep(10)

    # Parsing the content using the default python html parser
    soup = BeautifulSoup(browser.page_source, 'html.parser')

    # Removing script tag for visiblitly
    [s.extract() for s in soup('script')]

    # Declaring the 2 lists to hold them all
    home_fixtures = list()
    away_fixtures = list()

    # =============
    # Scraping
    # =============

    # Home & Away clubs
    home = soup.find('div', {'class': 'match-centre-header-team',
                             'data-field': 'home'}).a.get_text()
    home_fixtures.append(home)

    away = soup.find('div', {'class': 'match-centre-header-team',
                             'data-field': 'away'}).a.get_text()
    away_fixtures.append(away)

    # As per tarans excel
    home_fixtures.append(0)
    away_fixtures.append(1)

    home_fixtures.append(away)
    away_fixtures.append(home)

    home_fixtures.append(match.week)
    away_fixtures.append(match.week)

    # SHOTS -> RESULTS

    # Shots -> Results -> Goals
    shots_results_goals_home = soup.find(
        'div', {'data-filter-index': '0_0_0'})('span')[0].get_text()
    home_fixtures.append(shots_results_goals_home)

    shots_results_goals_away = soup.find(
        'div', {'data-filter-index': '0_0_0'})('span')[1].get_text()
    away_fixtures.append(shots_results_goals_away)

    # Shots -> Results -> Shots on Target
    shots_results_ontarget_home = soup.find(
        'div', {'data-filter-index': '0_0_1'})('span')[0].get_text()
    home_fixtures.append(shots_results_ontarget_home)

    shots_results_ontarget_away = soup.find(
        'div', {'data-filter-index': '0_0_1'})('span')[1].get_text()
    away_fixtures.append(shots_results_ontarget_away)

    # Shots -> Results -> Shots off Target
    shots_results_offtarget_home = soup.find(
        'div', {'data-filter-index': '0_0_2'})('span')[0].get_text()
    home_fixtures.append(shots_results_offtarget_home)

    shots_results_offtarget_away = soup.find(
        'div', {'data-filter-index': '0_0_2'})('span')[1].get_text()
    away_fixtures.append(shots_results_offtarget_away)

    # Shots -> Results -> Woodwork
    shots_results_woodwork_home = soup.find(
        'div', {'data-filter-index': '0_0_3'})('span')[0].get_text()
    home_fixtures.append(shots_results_woodwork_home)

    shots_results_woodwork_away = soup.find(
        'div', {'data-filter-index': '0_0_3'})('span')[1].get_text()
    away_fixtures.append(shots_results_woodwork_away)

    # Shots -> Results -> Blocked
    shots_results_blocked_home = soup.find(
        'div', {'data-filter-index': '0_0_4'})('span')[0].get_text()
    home_fixtures.append(shots_results_blocked_home)

    shots_results_blocked_away = soup.find(
        'div', {'data-filter-index': '0_0_4'})('span')[1].get_text()
    away_fixtures.append(shots_results_blocked_away)

    # Shots -> Results -> Own
    shots_results_own_home = soup.find(
        'div', {'data-filter-index': '0_0_5'})('span')[0].get_text()
    home_fixtures.append(shots_results_own_home)

    shots_results_own_away = soup.find(
        'div', {'data-filter-index': '0_0_5'})('span')[1].get_text()
    away_fixtures.append(shots_results_own_away)

    # SHOTS -> ZONES

    # Shots -> Zones -> 6-yard box
    shots_zones_6yard_home = soup.find(
        'div', {'data-filter-index': '0_1_0'})('span')[0].get_text()
    home_fixtures.append(shots_zones_6yard_home)

    shots_zones_6yard_away = soup.find(
        'div', {'data-filter-index': '0_1_1'})('span')[1].get_text()
    away_fixtures.append(shots_zones_6yard_away)

    # Shots -> Zones -> Penalty Area
    shots_zones_penalty_home = soup.find(
        'div', {'data-filter-index': '0_1_2'})('span')[0].get_text()
    home_fixtures.append(shots_zones_penalty_home)

    shots_zones_penalty_away = soup.find(
        'div', {'data-filter-index': '0_1_2'})('span')[1].get_text()
    away_fixtures.append(shots_zones_penalty_away)

    # Shots -> Zones -> Outside of Box
    shots_zones_ob_home = soup.find(
        'div', {'data-filter-index': '0_1_2'})('span')[0].get_text()
    home_fixtures.append(shots_zones_ob_home)

    shots_zones_ob_away = soup.find(
        'div', {'data-filter-index': '0_1_2'})('span')[1].get_text()
    away_fixtures.append(shots_zones_ob_away)

    # SHOTS -> SITUATION

    # Shots -> Situation -> 6-yard box
    shots_situation_open_home = soup.find(
        'div', {'data-filter-index': '0_2_0'})('span')[0].get_text()
    home_fixtures.append(shots_situation_open_home)

    shots_situation_open_away = soup.find(
        'div', {'data-filter-index': '0_2_0'})('span')[1].get_text()
    away_fixtures.append(shots_situation_open_away)

    # Shots -> Situation -> Penalty Area
    shots_situation_fastbreak_home = soup.find(
        'div', {'data-filter-index': '0_2_1'})('span')[0].get_text()
    home_fixtures.append(shots_situation_fastbreak_home)

    shots_situation_fastbreak_away = soup.find(
        'div', {'data-filter-index': '0_2_1'})('span')[1].get_text()
    away_fixtures.append(shots_situation_fastbreak_away)

    # Shots -> Situation -> Outside of Box
    shots_situation_set_home = soup.find(
        'div', {'data-filter-index': '0_2_2'})('span')[0].get_text()
    home_fixtures.append(shots_situation_set_home)

    shots_situation_set_away = soup.find(
        'div', {'data-filter-index': '0_2_2'})('span')[1].get_text()
    away_fixtures.append(shots_situation_set_away)

    # Shots -> Situation -> 6-yard box
    shots_situation_penalty_home = soup.find(
        'div', {'data-filter-index': '0_2_3'})('span')[0].get_text()
    home_fixtures.append(shots_situation_penalty_home)

    shots_situation_penalty_away = soup.find(
        'div', {'data-filter-index': '0_2_3'})('span')[1].get_text()
    away_fixtures.append(shots_situation_penalty_away)

    # Shots -> Situation -> Penalty Area
    shots_situation_goals_home = soup.find(
        'div', {'data-filter-index': '0_2_4'})('span')[0].get_text()
    home_fixtures.append(shots_situation_goals_home)

    shots_situation_goals_away = soup.find(
        'div', {'data-filter-index': '0_2_4'})('span')[1].get_text()
    away_fixtures.append(shots_situation_goals_away)

    # SHOTS -> BODY PARTS

    # Shots -> Body Parts -> Penalty Area
    shots_bp_rfoot_home = soup.find(
        'div', {'data-filter-index': '0_3_0'})('span')[0].get_text()
    home_fixtures.append(shots_bp_rfoot_home)

    shots_bp_rfoot_away = soup.find(
        'div', {'data-filter-index': '0_3_0'})('span')[1].get_text()
    away_fixtures.append(shots_bp_rfoot_away)

    # Shots -> Body Parts -> Outside of Box
    shots_bp_lfoot_home = soup.find(
        'div', {'data-filter-index': '0_3_1'})('span')[0].get_text()
    home_fixtures.append(shots_bp_lfoot_home)

    shots_bp_lfoot_away = soup.find(
        'div', {'data-filter-index': '0_3_1'})('span')[1].get_text()
    away_fixtures.append(shots_bp_lfoot_away)

    # Shots -> Body Parts -> 6-yard box
    shots_bp_head_home = soup.find(
        'div', {'data-filter-index': '0_3_2'})('span')[0].get_text()
    home_fixtures.append(shots_bp_head_home)

    shots_bp_head_away = soup.find(
        'div', {'data-filter-index': '0_3_2'})('span')[1].get_text()
    away_fixtures.append(shots_bp_head_away)

    # Shots -> Body Parts -> Penalty Area
    shots_bp_other_home = soup.find(
        'div', {'data-filter-index': '0_3_3'})('span')[0].get_text()
    home_fixtures.append(shots_bp_other_home)

    shots_bp_other_away = soup.find(
        'div', {'data-filter-index': '0_3_3'})('span')[1].get_text()
    away_fixtures.append(shots_bp_other_away)

    # PASSES -> PASS TYPE

    # Passes -> Pass Type -> Cross
    pass_pt_cross_home = soup.find(
        'div', {'data-filter-index': '1_0_0'})('span')[0].get_text()
    home_fixtures.append(pass_pt_cross_home)

    pass_pt_cross_away = soup.find(
        'div', {'data-filter-index': '1_0_0'})('span')[1].get_text()
    away_fixtures.append(pass_pt_cross_away)

    # Passes -> Pass Type -> Freekick
    pass_pt_freekick_home = soup.find(
        'div', {'data-filter-index': '1_0_1'})('span')[0].get_text()
    home_fixtures.append(pass_pt_freekick_home)

    pass_pt_freekick_away = soup.find(
        'div', {'data-filter-index': '1_0_1'})('span')[1].get_text()
    away_fixtures.append(pass_pt_freekick_away)

    # Passes -> Pass Type -> Corner
    pass_pt_corner_home = soup.find(
        'div', {'data-filter-index': '1_0_2'})('span')[0].get_text()
    home_fixtures.append(pass_pt_corner_home)

    pass_pt_corner_away = soup.find(
        'div', {'data-filter-index': '1_0_2'})('span')[1].get_text()
    away_fixtures.append(pass_pt_corner_away)

    # Passes -> Pass Type -> Through Ball
    pass_pt_through_home = soup.find(
        'div', {'data-filter-index': '1_0_3'})('span')[0].get_text()
    home_fixtures.append(pass_pt_through_home)

    pass_pt_through_away = soup.find(
        'div', {'data-filter-index': '1_0_3'})('span')[1].get_text()
    away_fixtures.append(pass_pt_through_away)

    # Passes -> Pass Type -> Throw In
    pass_pt_throw_home = soup.find(
        'div', {'data-filter-index': '1_0_4'})('span')[0].get_text()
    home_fixtures.append(pass_pt_throw_home)

    pass_pt_throw_away = soup.find(
        'div', {'data-filter-index': '1_0_4'})('span')[1].get_text()
    away_fixtures.append(pass_pt_throw_away)

    # Passes -> Pass Type -> Key Passes
    pass_pt_key_home = soup.find(
        'div', {'data-filter-index': '1_0_5'})('span')[0].get_text()
    home_fixtures.append(pass_pt_key_home)

    pass_pt_key_away = soup.find(
        'div', {'data-filter-index': '1_0_5'})('span')[1].get_text()
    away_fixtures.append(pass_pt_key_away)

    # PASSES -> LENGTH

    # Passes -> Length -> Long
    pass_length_long_home = soup.find(
        'div', {'data-filter-index': '1_1_0'})('span')[0].get_text()
    home_fixtures.append(pass_length_long_home)

    pass_length_long_away = soup.find(
        'div', {'data-filter-index': '1_1_0'})('span')[1].get_text()
    away_fixtures.append(pass_length_long_away)

    # Passes -> Length -> Short
    pass_length_short_home = soup.find(
        'div', {'data-filter-index': '1_1_1'})('span')[0].get_text()
    home_fixtures.append(pass_length_short_home)

    pass_length_short_away = soup.find(
        'div', {'data-filter-index': '1_1_1'})('span')[1].get_text()
    away_fixtures.append(pass_length_short_away)

    # PASSES -> HEIGHT

    # Passes -> Height -> Chipped
    pass_height_chipped_home = soup.find(
        'div', {'data-filter-index': '1_2_0'})('span')[0].get_text()
    home_fixtures.append(pass_height_chipped_home)

    pass_height_chipped_away = soup.find(
        'div', {'data-filter-index': '1_2_0'})('span')[1].get_text()
    away_fixtures.append(pass_height_chipped_away)

    # Passes -> Height -> Ground
    pass_height_ground_home = soup.find(
        'div', {'data-filter-index': '1_2_1'})('span')[0].get_text()
    home_fixtures.append(pass_height_ground_home)

    pass_height_ground_away = soup.find(
        'div', {'data-filter-index': '1_2_1'})('span')[1].get_text()
    away_fixtures.append(pass_height_ground_away)

    # PASSES -> BODY PARTS

    # Passes -> Body Parts -> Head
    pass_bp_head_home = soup.find(
        'div', {'data-filter-index': '1_3_0'})('span')[0].get_text()
    home_fixtures.append(pass_bp_head_home)

    pass_bp_head_away = soup.find(
        'div', {'data-filter-index': '1_3_0'})('span')[1].get_text()
    away_fixtures.append(pass_bp_head_away)

    # Passes -> Body Parts -> Feet
    pass_bp_feet_home = soup.find(
        'div', {'data-filter-index': '1_3_1'})('span')[0].get_text()
    home_fixtures.append(pass_bp_feet_home)

    pass_bp_feet_away = soup.find(
        'div', {'data-filter-index': '1_3_1'})('span')[1].get_text()
    away_fixtures.append(pass_bp_feet_away)

    # PASSES -> DIRECTION

    # Passes -> Direction -> Forward
    pass_dir_forward_home = soup.find(
        'div', {'data-filter-index': '1_4_0'})('span')[0].get_text()
    home_fixtures.append(pass_dir_forward_home)

    pass_dir_forward_away = soup.find(
        'div', {'data-filter-index': '1_4_0'})('span')[1].get_text()
    away_fixtures.append(pass_dir_forward_away)

    # Passes -> Direction -> Backward
    pass_dir_backward_home = soup.find(
        'div', {'data-filter-index': '1_4_1'})('span')[0].get_text()
    home_fixtures.append(pass_dir_backward_home)

    pass_dir_backward_away = soup.find(
        'div', {'data-filter-index': '1_4_1'})('span')[1].get_text()
    away_fixtures.append(pass_dir_backward_away)

    # Passes -> Direction -> Left
    pass_dir_left_home = soup.find(
        'div', {'data-filter-index': '1_4_2'})('span')[0].get_text()
    home_fixtures.append(pass_dir_left_home)

    pass_dir_left_away = soup.find(
        'div', {'data-filter-index': '1_4_2'})('span')[1].get_text()
    away_fixtures.append(pass_dir_left_away)

    # Passes -> Direction -> Right
    pass_dir_right_home = soup.find(
        'div', {'data-filter-index': '1_4_3'})('span')[0].get_text()
    home_fixtures.append(pass_dir_right_home)

    pass_dir_right_away = soup.find(
        'div', {'data-filter-index': '1_4_3'})('span')[1].get_text()
    away_fixtures.append(pass_dir_right_away)

    # PASSES -> TARGET ZONE

    # Passes -> Target Zone -> Defensive Third
    pass_targetz_def_home = soup.find(
        'div', {'data-filter-index': '1_5_0'})('span')[0].get_text()
    home_fixtures.append(pass_targetz_def_home)

    pass_targetz_def_away = soup.find(
        'div', {'data-filter-index': '1_5_0'})('span')[1].get_text()
    away_fixtures.append(pass_targetz_def_away)

    # Passes -> Target Zone -> Mid Third
    pass_targetz_mid_home = soup.find(
        'div', {'data-filter-index': '1_5_1'})('span')[0].get_text()
    home_fixtures.append(pass_targetz_mid_home)

    pass_targetz_mid_away = soup.find(
        'div', {'data-filter-index': '1_5_1'})('span')[1].get_text()
    away_fixtures.append(pass_targetz_mid_away)

    # Passes -> Target Zone -> Final Third
    pass_targetz_final_home = soup.find(
        'div', {'data-filter-index': '1_5_2'})('span')[0].get_text()
    home_fixtures.append(pass_targetz_final_home)

    pass_targetz_final_away = soup.find(
        'div', {'data-filter-index': '1_5_2'})('span')[1].get_text()
    away_fixtures.append(pass_targetz_final_away)

    # DRIBBLES -> OUTCOME

    # Dribbles -> Outcome -> Successful
    dribble_outcome_suc_home = soup.find(
        'div', {'data-filter-index': '2_0_0'})('span')[0].get_text()
    home_fixtures.append(dribble_outcome_suc_home)

    dribble_outcome_suc_away = soup.find(
        'div', {'data-filter-index': '2_0_0'})('span')[1].get_text()
    away_fixtures.append(dribble_outcome_suc_away)

    # Dribbles -> Outcome -> Unsuccesful
    dribble_outcome_un_home = soup.find(
        'div', {'data-filter-index': '2_0_1'})('span')[0].get_text()
    home_fixtures.append(dribble_outcome_un_home)

    dribble_outcome_un_away = soup.find(
        'div', {'data-filter-index': '2_0_1'})('span')[1].get_text()
    away_fixtures.append(dribble_outcome_un_away)

    # TACKES ATTEMPTED -> OUTCOME

    # Tackles Attempted -> Outcome -> Successful Tackles
    tackles_outcome_suc_home = soup.find(
        'div', {'data-filter-index': '3_0_0'})('span')[0].get_text()
    home_fixtures.append(tackles_outcome_suc_home)

    tackles_outcome_suc_away = soup.find(
        'div', {'data-filter-index': '3_0_0'})('span')[1].get_text()
    away_fixtures.append(tackles_outcome_suc_away)

    # Tackles Attempted -> Outcome -> Was Dribbled
    tackles_outcome_un_home = soup.find(
        'div', {'data-filter-index': '3_0_1'})('span')[0].get_text()
    home_fixtures.append(tackles_outcome_un_home)

    tackles_outcome_un_away = soup.find(
        'div', {'data-filter-index': '3_0_1'})('span')[1].get_text()
    away_fixtures.append(tackles_outcome_un_away)

    # INTERCEPTIONS

    intercpetions_home = soup.find(
        'li', {'data-filter-index': '4'})('span')[0].get_text()
    home_fixtures.append(intercpetions_home)

    intercpetions_away = soup.find(
        'li', {'data-filter-index': '4'})('span')[2].get_text()
    away_fixtures.append(intercpetions_away)

    # CLEARANCES

    # Clearances -> Outcome -> Total
    clear_outcome_total_home = soup.find(
        'div', {'data-filter-index': '5_0_0'})('span')[0].get_text()
    home_fixtures.append(clear_outcome_total_home)

    clear_outcome_total_away = soup.find(
        'div', {'data-filter-index': '5_0_0'})('span')[1].get_text()
    away_fixtures.append(clear_outcome_total_away)

    # Clearances -> Outcome -> Off The Line
    clear_outcome_otl_home = soup.find(
        'div', {'data-filter-index': '5_0_1'})('span')[0].get_text()
    home_fixtures.append(clear_outcome_otl_home)

    clear_outcome_otl_away = soup.find(
        'div', {'data-filter-index': '5_0_1'})('span')[1].get_text()
    away_fixtures.append(clear_outcome_otl_away)

    # Clearances -> Body Parts -> Head
    clear_bp_head_home = soup.find(
        'div', {'data-filter-index': '5_1_0'})('span')[0].get_text()
    home_fixtures.append(clear_bp_head_home)

    clear_bp_head_away = soup.find(
        'div', {'data-filter-index': '5_1_0'})('span')[1].get_text()
    away_fixtures.append(clear_bp_head_away)

    # Clearances -> Body Parts -> Feet
    clear_bp_feet_home = soup.find(
        'div', {'data-filter-index': '5_1_1'})('span')[0].get_text()
    home_fixtures.append(clear_bp_feet_home)

    clear_bp_feet_away = soup.find(
        'div', {'data-filter-index': '5_1_1'})('span')[1].get_text()
    away_fixtures.append(clear_bp_feet_away)

    # BLOCKS -> TYPE

    # Blocks -> Type -> Blocked Shots
    blocks_type_blocked_home = soup.find(
        'div', {'data-filter-index': '6_0_0'})('span')[0].get_text()
    home_fixtures.append(blocks_type_blocked_home)

    blocks_type_blocked_away = soup.find(
        'div', {'data-filter-index': '6_0_0'})('span')[1].get_text()
    away_fixtures.append(blocks_type_blocked_away)

    # Blocks -> Type -> Crosses
    blocks_type_crosses_home = soup.find(
        'div', {'data-filter-index': '6_0_1'})('span')[0].get_text()
    home_fixtures.append(blocks_type_crosses_home)

    blocks_type_crosses_away = soup.find(
        'div', {'data-filter-index': '6_0_1'})('span')[1].get_text()
    away_fixtures.append(blocks_type_crosses_away)

    # FOULS

    fouls_home = soup.find(
        'li', {'data-filter-index': '8'})('span')[0].get_text()
    home_fixtures.append(fouls_home)

    fouls_away = soup.find(
        'li', {'data-filter-index': '8'})('span')[2].get_text()
    away_fixtures.append(fouls_away)

    # ARIEL DUELS

    ariel_home = soup.find(
        'li', {'data-filter-index': '9'})('span')[0].get_text()
    home_fixtures.append(ariel_home)

    ariel_away = soup.find(
        'li', {'data-filter-index': '9'})('span')[2].get_text()
    away_fixtures.append(ariel_away)

    # TOUCHES

    touches_home = soup.find(
        'li', {'data-filter-index': '10'})('span')[0].get_text()
    home_fixtures.append(touches_home)

    touches_away = soup.find(
        'li', {'data-filter-index': '10'})('span')[2].get_text()
    away_fixtures.append(touches_away)

    # LOSS OF POSSESSION

    # Loss of possession -> Type -> Dispossessed
    lop_type_dispossessed_home = soup.find(
        'div', {'data-filter-index': '11_0_0'})('span')[0].get_text()
    home_fixtures.append(lop_type_dispossessed_home)

    lop_type_dispossessed_away = soup.find(
        'div', {'data-filter-index': '11_0_0'})('span')[1].get_text()
    away_fixtures.append(lop_type_dispossessed_away)

    # Loss of possession -> type -> Turnover
    lop_type_turnover_home = soup.find(
        'div', {'data-filter-index': '11_0_1'})('span')[0].get_text()
    home_fixtures.append(lop_type_turnover_home)

    lop_type_turnover_away = soup.find(
        'div', {'data-filter-index': '11_0_1'})('span')[1].get_text()
    away_fixtures.append(lop_type_turnover_away)

    # ERRORS

    # Errors -> Type -> Lead to Shot
    errors_type_shot_home = soup.find(
        'div', {'data-filter-index': '12_0_0'})('span')[0].get_text()
    home_fixtures.append(errors_type_shot_home)

    errors_type_shot_away = soup.find(
        'div', {'data-filter-index': '12_0_0'})('span')[1].get_text()
    away_fixtures.append(errors_type_shot_away)

    # Errors -> type -> Lead to Goal
    errors_type_goal_home = soup.find(
        'div', {'data-filter-index': '12_0_1'})('span')[0].get_text()
    home_fixtures.append(errors_type_goal_home)

    errors_type_goal_away = soup.find(
        'div', {'data-filter-index': '12_0_1'})('span')[1].get_text()
    away_fixtures.append(errors_type_goal_away)

    # SAVES

    saves_home = soup.find(
        'li', {'data-filter-index': '13'})('span')[0].get_text()
    home_fixtures.append(saves_home)

    saves_away = soup.find(
        'li', {'data-filter-index': '13'})('span')[2].get_text()
    away_fixtures.append(saves_away)

    # CLAIMS

    claims_home = soup.find(
        'li', {'data-filter-index': '14'})('span')[0].get_text()
    home_fixtures.append(claims_home)

    claims_away = soup.find(
        'li', {'data-filter-index': '14'})('span')[2].get_text()
    away_fixtures.append(claims_away)

    # PUNCHES

    punches_home = soup.find(
        'li', {'data-filter-index': '15'})('span')[0].get_text()
    home_fixtures.append(punches_home)

    punches_away = soup.find(
        'li', {'data-filter-index': '15'})('span')[2].get_text()
    away_fixtures.append(punches_away)

    print "\nCompleted: " + home + " vs. " + away + "\n"

    if verbose:
        # If True then print info
        print '{:20} {:^10} {:^10}'.format('STATS', 'HOME', 'AWAY')
        print "\n----- Shots -----\n"
        print '{:20} {:^10} {:^10}'.format('team', home, away)
        print '{:20} {:^10} {:^10}'.format(
            'goals', shots_results_goals_home, shots_results_goals_away)
        print '{:20} {:^10} {:^10}'.format(
            'on target',
            shots_results_ontarget_home,
            shots_results_ontarget_away)
        print '{:20} {:^10} {:^10}'.format(
            'off target',
            shots_results_offtarget_home,
            shots_results_offtarget_away)
        print '{:20} {:^10} {:^10}'.format(
            'woodwork',
            shots_results_woodwork_home,
            shots_results_woodwork_away)
        print '{:20} {:^10} {:^10}'.format(
            'blocked', shots_results_blocked_home, shots_results_blocked_away)
        print '{:20} {:^10} {:^10}'.format(
            'own goals', shots_results_own_home, shots_results_own_away)
        print '{:20} {:^10} {:^10}'.format(
            '6 yard box', shots_zones_6yard_home, shots_zones_6yard_away)
        print '{:20} {:^10} {:^10}'.format(
            'penalty area', shots_zones_penalty_home, shots_zones_penalty_away)
        print '{:20} {:^10} {:^10}'.format(
            'outside box', shots_zones_ob_home, shots_zones_ob_away)
        print '{:20} {:^10} {:^10}'.format(
            'open play', shots_situation_open_home, shots_situation_open_away)
        print '{:20} {:^10} {:^10}'.format(
            'fast break',
            shots_situation_fastbreak_home,
            shots_situation_fastbreak_away)
        print '{:20} {:^10} {:^10}'.format(
            'set pieces', shots_situation_set_home, shots_situation_set_away)
        print '{:20} {:^10} {:^10}'.format(
            'penalty',
            shots_situation_penalty_home,
            shots_situation_penalty_away)
        print '{:20} {:^10} {:^10}'.format(
            'right foot', shots_bp_rfoot_home, shots_bp_rfoot_away)
        print '{:20} {:^10} {:^10}'.format(
            'left foot', shots_bp_lfoot_home, shots_bp_lfoot_away)
        print '{:20} {:^10} {:^10}'.format(
            'head', shots_bp_head_home, shots_bp_head_away)
        print "\n----- Passes -----\n"
        print '{:20} {:^10} {:^10}'.format(
            'cross', pass_pt_cross_home, pass_pt_cross_away)
        print '{:20} {:^10} {:^10}'.format(
            'freekick', pass_pt_freekick_home, pass_pt_freekick_away)
        print '{:20} {:^10} {:^10}'.format(
            'corner', pass_pt_corner_home, pass_pt_corner_away)
        print '{:20} {:^10} {:^10}'.format(
            'through ball', pass_pt_through_home, pass_pt_through_away)
        print '{:20} {:^10} {:^10}'.format(
            'throw in', pass_pt_throw_home, pass_pt_throw_away)
        print '{:20} {:^10} {:^10}'.format(
            'key passes', pass_pt_key_home, pass_pt_key_away)
        print '{:20} {:^10} {:^10}'.format(
            'long', pass_length_long_home, pass_length_long_away)
        print '{:20} {:^10} {:^10}'.format(
            'short', pass_length_short_home, pass_length_short_away)
        print '{:20} {:^10} {:^10}'.format(
            'chipped', pass_height_chipped_home, pass_height_chipped_away)
        print '{:20} {:^10} {:^10}'.format(
            'ground', pass_height_ground_home, pass_height_ground_away)
        print '{:20} {:^10} {:^10}'.format(
            'head', pass_bp_head_home, pass_bp_head_away)
        print '{:20} {:^10} {:^10}'.format(
            'feet', pass_bp_feet_home, pass_bp_feet_away)
        print '{:20} {:^10} {:^10}'.format(
            'forward', pass_dir_forward_home, pass_dir_forward_away)
        print '{:20} {:^10} {:^10}'.format(
            'backward', pass_dir_backward_home, pass_dir_backward_away)
        print '{:20} {:^10} {:^10}'.format(
            'left', pass_dir_left_home, pass_dir_left_away)
        print '{:20} {:^10} {:^10}'.format(
            'right', pass_dir_right_home, pass_dir_right_away)
        print '{:20} {:^10} {:^10}'.format(
            'defensive', pass_targetz_def_home, pass_targetz_def_away)
        print '{:20} {:^10} {:^10}'.format(
            'mid', pass_targetz_mid_home, pass_targetz_mid_away)
        print '{:20} {:^10} {:^10}'.format(
            'final', pass_targetz_final_away, pass_targetz_final_away)
        print "\n----- Dribbles -----\n"
        print '{:20} {:^10} {:^10}'.format(
            'successful', dribble_outcome_suc_home, dribble_outcome_suc_away)
        print '{:20} {:^10} {:^10}'.format(
            'unsuccessful', dribble_outcome_un_home, dribble_outcome_un_away)
        print "\n----- Tackles Attempted -----\n"
        print '{:20} {:^10} {:^10}'.format(
            'successful', tackles_outcome_suc_home, tackles_outcome_suc_away)
        print '{:20} {:^10} {:^10}'.format(
            'unsuccessful', tackles_outcome_un_home, tackles_outcome_un_away)
        print "\n----- Interceptions -----\n"
        print '{:20} {:^10} {:^10}'.format(
            'interceptions', intercpetions_home, intercpetions_away)
        print "\n----- Clearances -----\n"
        print '{:20} {:^10} {:^10}'.format(
            'total', clear_outcome_total_home, clear_outcome_total_away)
        print '{:20} {:^10} {:^10}'.format(
            'off the line', clear_outcome_otl_home, clear_outcome_otl_away)
        print '{:20} {:^10} {:^10}'.format(
            'head', clear_bp_head_home, clear_bp_head_away)
        print '{:20} {:^10} {:^10}'.format(
            'feet', clear_bp_feet_home, clear_bp_feet_away)
        print "\n----- Blocks -----\n"
        print '{:20} {:^10} {:^10}'.format(
            'blocked shots',
            blocks_type_blocked_home,
            blocks_type_blocked_away)
        print '{:20} {:^10} {:^10}'.format(
            'crosses', blocks_type_crosses_home, blocks_type_crosses_away)
        print "\n----- Fouls -----\n"
        print '{:20} {:^10} {:^10}'.format(
            'fouls', fouls_home, fouls_away)
        print "\n----- Ariel Duels -----\n"
        print '{:20} {:^10} {:^10}'.format(
            'ariel duels', ariel_home, ariel_away)
        print "\n----- Touches -----\n"
        print '{:20} {:^10} {:^10}'.format(
            'touches', touches_home, touches_away)
        print "\n----- Loss of Possession -----\n"
        print '{:20} {:^10} {:^10}'.format(
            'dispossessed', blocks_type_blocked_home, blocks_type_blocked_away)
        print '{:20} {:^10} {:^10}'.format(
            'turnover', blocks_type_crosses_home, blocks_type_crosses_away)
        print "\n----- Errors -----\n"
        print '{:20} {:^10} {:^10}'.format(
            'lead to shot', errors_type_shot_home, errors_type_shot_away)
        print '{:20} {:^10} {:^10}'.format(
            'lead to goal', errors_type_goal_home, errors_type_goal_away)
        print "\n----- Saves -----\n"
        print '{:20} {:^10} {:^10}'.format(
            'saves', saves_home, saves_away)
        print "\n----- Claims -----\n"
        print '{:20} {:^10} {:^10}'.format(
            'claims', claims_home, claims_away)
        print "\n----- Punches -----\n"
        print '{:20} {:^10} {:^10}'.format(
            'punches', punches_home, punches_away)

        print "\n=============================================\n"

    # Write this fixture as a row to csv
    # Create the csv file if it does not exist
    with open("output.csv", "ab") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(home_fixtures)
        writer.writerow(away_fixtures)

# Stop the webkit browser process
browser.quit()

print "\nFinished!\n"
print "The output.csv file will be located in the same directory "
print "in which you ran this script.\n"

print "Exiting..."
raise SystemExit
