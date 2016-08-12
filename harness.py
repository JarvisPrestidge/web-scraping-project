# Jarvis Prestidge & Kanita Dogra
# Decription:   tbc

# Including imports

import collections
import platform
import os
import time

from datetime import timedelta, datetime

from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

# url to scrape
home_url = ("https://www.whoscored.com/Regions/252/Tournaments/2/Seasons/5826"
            "/Stages/12496/Fixtures/England-Premier-League-2015-2016")

print "\nWelcome to Taran's whoscored.com webscraping script.\n"

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

print "Getting html data"
browser = webdriver.PhantomJS(phantomjs_path)
browser.get(home_url)
time.sleep(5)

# Get handle to "previous" button
el = browser.find_element_by_xpath(
    '//a[@class="previous button ui-state-default rc-l is-default"]')

print "\nTravelling back in time...\n"

while True:

    # Perform click
    webdriver.ActionChains(browser).move_to_element(el).click(el).perform()

    # Attempting to give the browser enough time to load the page
    delay = 10
    try:
        WebDriverWait(browser, delay).until(
            EC.presence_of_element_located((
                By.ID, 'tournament-fixture-wrapper')))
        print "Page is ready!"
    except TimeoutException:
        print "Loading took too much time!"
    except Exception:
        print "Unknown exception occurred!"

    time.sleep(10)

    # Parsing the content using the default python html parser
    soup = BeautifulSoup(browser.page_source, 'html.parser')

    print soup.find(
        'a', {'id': 'date-config-toggle-button'})('span')[0].get_text() + "\n"

    if soup.find('a', {'class': 'previous button ui-state-default rc-l is-disabled'}) is None:
        continue
    else:
        break

print "Successfully reached start of season."

print "Removing scripts..."
# Removing script tag for visiblitly"
[s.extract() for s in soup('script')]


# =============
# Scraping
# =============

# Creating named tuple object to hold pertinent data
Fixtures = collections.namedtuple(
    'Fixtures', 'date week kickoff home away url')

print "\nCommencing fixture scraping per month.\n"


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

# Looping through each month
while True:
    print "Current month: " + soup.find(
        'a', {'id': 'date-config-toggle-button'})('span')[0].get_text()

    # Gathering list of all fixture rows
    rows = soup.find('table', id='tournament-fixture')('tr')

    print "\nFixtures captured: " + str(len(rows))

    for row in rows:
        # For each row we either append to 'Fixtures' or record date
        if row.find('th') is None:
            # Fixture - we collect pertinent info
            Fixtures(
                date=date_counter,
                week=week_counter,
                kickoff=row.find('td', {'class': 'time'}).get_text(),
                home=row('a', {'class': 'team-link '})[0].get_text(),
                away=row('a', {'class': 'team-link '})[1].get_text(),
                url=row.find(
                    'a', {'class': 'match-link match-report rc'}).get('href')
            )
            # somehow append this tuple to list
            continue
        else:
            # Date header - we log the current week & date
            week_counter = week(strtodate(row.get_text()))
            date_counter = row.get_text()
            continue

    # Check if this was the last page
    if break_check is True:
        # If true then quit the loop
        break

    # Get handle to "next" button
    el = browser.find_element_by_xpath(
        '//a[@class="next button ui-state-default rc-r is-default"]')

    print "\nMoving forward in time :D\n"

    # Perform click
    webdriver.ActionChains(browser).move_to_element(el).click(el).perform()

    # Attempting to give the browser enough time to load the page
    delay = 10
    try:
        WebDriverWait(browser, delay).until(
            EC.presence_of_element_located((
                By.ID, 'tournament-fixture-wrapper')))
        print "Page is ready!"
    except TimeoutException:
        print "Loading took too much time!"
    except Exception:
        print "Unknown exception occurred!"

    time.sleep(10)

    # Parsing the content using the default python html parser
    soup = BeautifulSoup(browser.page_source, 'html.parser')

    if soup.find('a', {'class': 'next button ui-state-default rc-r is-disabled'}) is None:
        break_check = True

print "Finished scraping fixture data!"
