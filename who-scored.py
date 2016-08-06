# Jarvis Prestidge & Kanita Dogra
# Decription:   tbc

# Including imports

import platform
import os
import time

from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

# url to scrape
url = ("https://www.whoscored.com/Matches/959761/Live/"
       "England-Premier-League-2015-2016-Swansea-Liverpool")

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
browser.get(url)
time.sleep(5)
el = browser.find_element_by_xpath('//a[@href="#chalkboard"]')
webdriver.ActionChains(browser).move_to_element(el).click(el).perform()

# Attempting to give the browser enough time to load the page
delay = 10
try:
    WebDriverWait(browser, delay).until(
        EC.presence_of_element_located((By.ID, 'chalkboard-timeline')))
    print "Page is ready!"
except TimeoutException:
    print "Loading took too much time!"
except Exception:
    print "Unknown exception occureed!"

browser.implicitly_wait(10)
time.sleep(10)

# Parsing the content using the default python html parser
soup = BeautifulSoup(browser.page_source, 'html.parser')

# Removing script tag for visiblitly
[s.extract() for s in soup('script')]


# =============
# Scraping
# =============

# Home & Away clubs
home = soup.find('div', {'class': 'match-centre-header-team',
                         'data-field': 'home'}).a.get_text()

away = soup.find('div', {'class': 'match-centre-header-team',
                         'data-field': 'away'}).a.get_text()

# SHOTS -> RESULTS

# Shots -> Results -> Goals
shots_results_goals_home = soup.find(
    'div', {'data-filter-index': '0_0_0'})('span')[0].get_text()

shots_results_goals_away = soup.find(
    'div', {'data-filter-index': '0_0_0'})('span')[1].get_text()

# Shots -> Results -> Shots on Target
shots_results_ontarget_home = soup.find(
    'div', {'data-filter-index': '0_0_1'})('span')[0].get_text()

shots_results_ontarget_away = soup.find(
    'div', {'data-filter-index': '0_0_1'})('span')[1].get_text()

# Shots -> Results -> Shots off Target
shots_results_offtarget_home = soup.find(
    'div', {'data-filter-index': '0_0_2'})('span')[0].get_text()

shots_results_offtarget_away = soup.find(
    'div', {'data-filter-index': '0_0_2'})('span')[1].get_text()

# Shots -> Results -> Woodwork
shots_results_woodwork_home = soup.find(
    'div', {'data-filter-index': '0_0_3'})('span')[0].get_text()

shots_results_woodwork_away = soup.find(
    'div', {'data-filter-index': '0_0_3'})('span')[1].get_text()

# Shots -> Results -> Blocked
shots_results_blocked_home = soup.find(
    'div', {'data-filter-index': '0_0_4'})('span')[0].get_text()

shots_results_blocked_away = soup.find(
    'div', {'data-filter-index': '0_0_4'})('span')[1].get_text()

# Shots -> Results -> Own
shots_results_own_home = soup.find(
    'div', {'data-filter-index': '0_0_5'})('span')[0].get_text()

shots_results_own_away = soup.find(
    'div', {'data-filter-index': '0_0_5'})('span')[1].get_text()

# SHOTS -> ZONES

# Shots -> Zones -> 6-yard box
shots_zones_6yard_home = soup.find(
    'div', {'data-filter-index': '0_1_0'})('span')[0].get_text()

shots_zones_6yard_away = soup.find(
    'div', {'data-filter-index': '0_1_1'})('span')[1].get_text()

# Shots -> Zones -> Penalty Area
shots_zones_penalty_home = soup.find(
    'div', {'data-filter-index': '0_1_2'})('span')[0].get_text()

shots_zones_penalty_away = soup.find(
    'div', {'data-filter-index': '0_1_2'})('span')[1].get_text()

# Shots -> Zones -> Outside of Box
shots_zones_ob_home = soup.find(
    'div', {'data-filter-index': '0_1_2'})('span')[0].get_text()

shots_zones_ob_away = soup.find(
    'div', {'data-filter-index': '0_1_2'})('span')[1].get_text()

# SHOTS -> SITUATION

# Shots -> Situation -> 6-yard box
shots_situation_open_home = soup.find(
    'div', {'data-filter-index': '0_2_0'})('span')[0].get_text()

shots_situation_open_away = soup.find(
    'div', {'data-filter-index': '0_2_0'})('span')[1].get_text()

# Shots -> Situation -> Penalty Area
shots_situation_fastbreak_home = soup.find(
    'div', {'data-filter-index': '0_2_1'})('span')[0].get_text()

shots_situation_fastbreak_away = soup.find(
    'div', {'data-filter-index': '0_2_1'})('span')[1].get_text()

# Shots -> Situation -> Outside of Box
shots_situation_set_home = soup.find(
    'div', {'data-filter-index': '0_2_2'})('span')[0].get_text()

shots_situation_set_away = soup.find(
    'div', {'data-filter-index': '0_2_2'})('span')[1].get_text()

# Shots -> Situation -> 6-yard box
shots_situation_penalty_home = soup.find(
    'div', {'data-filter-index': '0_2_3'})('span')[0].get_text()

shots_situation_penalty_away = soup.find(
    'div', {'data-filter-index': '0_2_3'})('span')[1].get_text()

# Shots -> Situation -> Penalty Area
shots_situation_goals_home = soup.find(
    'div', {'data-filter-index': '0_2_4'})('span')[0].get_text()

shots_situation_goals_away = soup.find(
    'div', {'data-filter-index': '0_2_4'})('span')[1].get_text()

# SHOTS -> BODY PARTS

# Shots -> Body Parts -> Penalty Area
shots_bp_rfoot_home = soup.find(
    'div', {'data-filter-index': '0_3_0'})('span')[0].get_text()

shots_bp_rfoot_away = soup.find(
    'div', {'data-filter-index': '0_3_0'})('span')[1].get_text()

# Shots -> Body Parts -> Outside of Box
shots_bp_lfoot_home = soup.find(
    'div', {'data-filter-index': '0_3_1'})('span')[0].get_text()

shots_bp_lfoot_away = soup.find(
    'div', {'data-filter-index': '0_3_1'})('span')[1].get_text()

# Shots -> Body Parts -> 6-yard box
shots_bp_head_home = soup.find(
    'div', {'data-filter-index': '0_3_2'})('span')[0].get_text()

shots_bp_head_away = soup.find(
    'div', {'data-filter-index': '0_3_2'})('span')[1].get_text()

# Shots -> Body Parts -> Penalty Area
shots_bp_other_home = soup.find(
    'div', {'data-filter-index': '0_3_3'})('span')[0].get_text()

shots_bp_other_away = soup.find(
    'div', {'data-filter-index': '0_3_3'})('span')[1].get_text()

# PASSES -> PASS TYPE

# Passes -> Pass Type -> Cross
pass_pt_cross_home = soup.find(
    'div', {'data-filter-index': '1_0_0'})('span')[0].get_text()

pass_pt_cross_away = soup.find(
    'div', {'data-filter-index': '1_0_0'})('span')[1].get_text()

# Passes -> Pass Type -> Freekick
pass_pt_freekick_home = soup.find(
    'div', {'data-filter-index': '1_0_1'})('span')[0].get_text()

pass_pt_freekick_away = soup.find(
    'div', {'data-filter-index': '1_0_1'})('span')[1].get_text()

# Passes -> Pass Type -> Corner
pass_pt_corner_home = soup.find(
    'div', {'data-filter-index': '1_0_2'})('span')[0].get_text()

pass_pt_corner_away = soup.find(
    'div', {'data-filter-index': '1_0_2'})('span')[1].get_text()

# Passes -> Pass Type -> Through Ball
pass_pt_through_home = soup.find(
    'div', {'data-filter-index': '1_0_3'})('span')[0].get_text()

pass_pt_through_away = soup.find(
    'div', {'data-filter-index': '1_0_3'})('span')[1].get_text()

# Passes -> Pass Type -> Throw In
pass_pt_throw_home = soup.find(
    'div', {'data-filter-index': '1_0_4'})('span')[0].get_text()

pass_pt_throw_away = soup.find(
    'div', {'data-filter-index': '1_0_4'})('span')[1].get_text()

# Passes -> Pass Type -> Key Passes
pass_pt_key_home = soup.find(
    'div', {'data-filter-index': '1_0_5'})('span')[0].get_text()

pass_pt_key_away = soup.find(
    'div', {'data-filter-index': '1_0_5'})('span')[1].get_text()

# PASSES -> LENGTH

# Passes -> Length -> Long
pass_length_long_home = soup.find(
    'div', {'data-filter-index': '1_1_0'})('span')[0].get_text()

pass_length_long_away = soup.find(
    'div', {'data-filter-index': '1_1_0'})('span')[1].get_text()

# Passes -> Length -> Short
pass_length_short_home = soup.find(
    'div', {'data-filter-index': '1_1_1'})('span')[0].get_text()

pass_length_short_away = soup.find(
    'div', {'data-filter-index': '1_1_1'})('span')[1].get_text()

# PASSES -> HEIGHT

# Passes -> Height -> Chipped
pass_height_chipped_home = soup.find(
    'div', {'data-filter-index': '1_2_0'})('span')[0].get_text()

pass_height_chipped_away = soup.find(
    'div', {'data-filter-index': '1_2_0'})('span')[1].get_text()

# Passes -> Height -> Ground
pass_height_ground_home = soup.find(
    'div', {'data-filter-index': '1_2_1'})('span')[0].get_text()

pass_height_ground_away = soup.find(
    'div', {'data-filter-index': '1_2_1'})('span')[1].get_text()

# PASSES -> BODY PARTS

# Passes -> Body Parts -> Head
pass_bp_head_home = soup.find(
    'div', {'data-filter-index': '1_3_0'})('span')[0].get_text()

pass_bp_head_away = soup.find(
    'div', {'data-filter-index': '1_3_0'})('span')[1].get_text()

# Passes -> Body Parts -> Feet
pass_bp_feet_home = soup.find(
    'div', {'data-filter-index': '1_3_1'})('span')[0].get_text()

pass_bp_feet_away = soup.find(
    'div', {'data-filter-index': '1_3_1'})('span')[1].get_text()

# PASSES -> DIRECTION

# Passes -> Direction -> Forward
pass_dir_forward_home = soup.find(
    'div', {'data-filter-index': '1_4_0'})('span')[0].get_text()

pass_dir_forward_away = soup.find(
    'div', {'data-filter-index': '1_4_0'})('span')[1].get_text()

# Passes -> Direction -> Backward
pass_dir_backward_home = soup.find(
    'div', {'data-filter-index': '1_4_1'})('span')[0].get_text()

pass_dir_backward_away = soup.find(
    'div', {'data-filter-index': '1_4_1'})('span')[1].get_text()

# Passes -> Direction -> Left
pass_dir_left_home = soup.find(
    'div', {'data-filter-index': '1_4_2'})('span')[0].get_text()

pass_dir_left_away = soup.find(
    'div', {'data-filter-index': '1_4_2'})('span')[1].get_text()

# Passes -> Direction -> Right
pass_dir_right_home = soup.find(
    'div', {'data-filter-index': '1_4_3'})('span')[0].get_text()

pass_dir_right_away = soup.find(
    'div', {'data-filter-index': '1_4_3'})('span')[1].get_text()

# PASSES -> TARGET ZONE

# Passes -> Target Zone -> Defensive Third
pass_targetz_def_home = soup.find(
    'div', {'data-filter-index': '1_5_0'})('span')[0].get_text()

pass_targetz_def_away = soup.find(
    'div', {'data-filter-index': '1_5_0'})('span')[1].get_text()

# Passes -> Target Zone -> Mid Third
pass_targetz_mid_home = soup.find(
    'div', {'data-filter-index': '1_5_1'})('span')[0].get_text()

pass_targetz_mid_away = soup.find(
    'div', {'data-filter-index': '1_5_1'})('span')[1].get_text()

# Passes -> Target Zone -> Final Third
pass_targetz_final_home = soup.find(
    'div', {'data-filter-index': '1_5_2'})('span')[0].get_text()

pass_targetz_final_away = soup.find(
    'div', {'data-filter-index': '1_5_2'})('span')[1].get_text()

# DRIBBLES -> OUTCOME

# Dribbles -> Outcome -> Successful
dribble_outcome_suc_home = soup.find(
    'div', {'data-filter-index': '2_0_0'})('span')[0].get_text()

dribble_outcome_suc_away = soup.find(
    'div', {'data-filter-index': '2_0_0'})('span')[1].get_text()

# Dribbles -> Outcome -> Unsuccesful
dribble_outcome_un_home = soup.find(
    'div', {'data-filter-index': '2_0_1'})('span')[0].get_text()

dribble_outcome_un_away = soup.find(
    'div', {'data-filter-index': '2_0_1'})('span')[1].get_text()


# TACKES ATTEMPTED -> OUTCOME

# Tackles Attempted -> Outcome -> Successful Tackles
tackles_outcome_suc_home = soup.find(
    'div', {'data-filter-index': '3_0_0'})('span')[0].get_text()

tackles_outcome_suc_away = soup.find(
    'div', {'data-filter-index': '3_0_0'})('span')[1].get_text()

# Tackles Attempted -> Outcome -> Was Dribbled
tackles_outcome_un_home = soup.find(
    'div', {'data-filter-index': '3_0_1'})('span')[0].get_text()

tackles_outcome_un_away = soup.find(
    'div', {'data-filter-index': '3_0_1'})('span')[1].get_text()

# INTERCEPTIONS

intercpetions_home = soup.find('li', {'data-filter-index': '4'})('span')[0].get_text()

intercpetions_away = soup.find('li', {'data-filter-index': '4'})('span')[2].get_text()

print "\n=============================================\n"
print '{:20} {:^10} {:^10}'.format('STAT', 'HOME', 'AWAY')
print "\n----- SHOTS -----\n"
print '{:20} {:^10} {:^10}'.format('team', home, away)
print '{:20} {:^10} {:^10}'.format('goals', shots_results_goals_home, shots_results_goals_away)
print '{:20} {:^10} {:^10}'.format('on target', shots_results_ontarget_home, shots_results_ontarget_away)
print '{:20} {:^10} {:^10}'.format('off target', shots_results_offtarget_home, shots_results_offtarget_away)
print '{:20} {:^10} {:^10}'.format('woodwork', shots_results_woodwork_home, shots_results_woodwork_away)
print '{:20} {:^10} {:^10}'.format('blocked', shots_results_blocked_home, shots_results_blocked_away)
print '{:20} {:^10} {:^10}'.format('own goals', shots_results_own_home, shots_results_own_away)
print '{:20} {:^10} {:^10}'.format('6 yard box', shots_zones_6yard_home, shots_zones_6yard_away)
print '{:20} {:^10} {:^10}'.format('penalty area', shots_zones_penalty_home, shots_zones_penalty_away)
print '{:20} {:^10} {:^10}'.format('outside box', shots_zones_ob_home, shots_zones_ob_away)
print '{:20} {:^10} {:^10}'.format('open play', shots_situation_open_home, shots_situation_open_away)
print '{:20} {:^10} {:^10}'.format('fast break', shots_situation_fastbreak_home, shots_situation_fastbreak_away)
print '{:20} {:^10} {:^10}'.format('set pieces', shots_situation_set_home, shots_situation_set_away)
print '{:20} {:^10} {:^10}'.format('penalty', shots_situation_penalty_home, shots_situation_penalty_away)
print '{:20} {:^10} {:^10}'.format('right foot', shots_bp_rfoot_home, shots_bp_rfoot_away)
print '{:20} {:^10} {:^10}'.format('left foot', shots_bp_lfoot_home, shots_bp_lfoot_away)
print '{:20} {:^10} {:^10}'.format('head', shots_bp_head_home, shots_bp_head_away)
print "\n----- PASSES -----\n"
print '{:20} {:^10} {:^10}'.format('cross', pass_pt_cross_home, pass_pt_cross_away)
print '{:20} {:^10} {:^10}'.format('freekick', pass_pt_freekick_home, pass_pt_freekick_away)
print '{:20} {:^10} {:^10}'.format('corner', pass_pt_corner_home, pass_pt_corner_away)
print '{:20} {:^10} {:^10}'.format('through ball', pass_pt_through_home, pass_pt_through_away)
print '{:20} {:^10} {:^10}'.format('throw in', pass_pt_throw_home, pass_pt_throw_away)
print '{:20} {:^10} {:^10}'.format('key passes', pass_pt_key_home, pass_pt_key_away)
print '{:20} {:^10} {:^10}'.format('long', pass_length_long_home, pass_length_long_away)
print '{:20} {:^10} {:^10}'.format('short', pass_length_short_home, pass_length_short_away)
print '{:20} {:^10} {:^10}'.format('chipped', pass_height_chipped_home, pass_height_chipped_away)
print '{:20} {:^10} {:^10}'.format('ground', pass_height_ground_home, pass_height_ground_away)
print '{:20} {:^10} {:^10}'.format('head', pass_bp_head_home, pass_bp_head_away)
print '{:20} {:^10} {:^10}'.format('feet', pass_bp_feet_home, pass_bp_feet_away)
print '{:20} {:^10} {:^10}'.format('forward', pass_dir_forward_home, pass_dir_forward_away)
print '{:20} {:^10} {:^10}'.format('backward', pass_dir_backward_home, pass_dir_backward_away)
print '{:20} {:^10} {:^10}'.format('left', pass_dir_left_home, pass_dir_left_away)
print '{:20} {:^10} {:^10}'.format('right', pass_dir_right_home, pass_dir_right_away)
print '{:20} {:^10} {:^10}'.format('defensive', pass_targetz_def_home, pass_targetz_def_away)
print '{:20} {:^10} {:^10}'.format('mid', pass_targetz_mid_home, pass_targetz_mid_away)
print '{:20} {:^10} {:^10}'.format('final', pass_targetz_final_away, pass_targetz_final_away)
print "\n----- DRIBBLES -----\n"
print '{:20} {:^10} {:^10}'.format('successful', dribble_outcome_suc_home, dribble_outcome_suc_away)
print '{:20} {:^10} {:^10}'.format('unsuccessful', dribble_outcome_un_home, dribble_outcome_un_away)
print "\n----- TACKLES ATTEMPTED -----\n"
print '{:20} {:^10} {:^10}'.format('successful', tackles_outcome_suc_home, tackles_outcome_suc_away)
print '{:20} {:^10} {:^10}'.format('unsuccessful', tackles_outcome_un_home, tackles_outcome_un_away)
print "\n----- INTERCEPTIONS -----\n"
print '{:20} {:^10} {:^10}'.format('interceptions', intercpetions_home, intercpetions_away)


browser.quit()
