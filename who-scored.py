# Jarvis Prestidge & Kanita Dogra
# Decription:   tbc

# Including imports

import platform
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

# PhantomJS files have different extensions
# under different operating systems
if platform.system() == 'Windows':
    phantomjs_path = './phantomjs.exe'
else:
    phantomjs_path = './phantomjs'

print "Path: " + phantomjs_path

browser = webdriver.PhantomJS(phantomjs_path)
browser.get(url)
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

shots_situation_goals_away = soup.find(
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

print "home team: " + home
print "away team: " + away
print "home goals:" + shots_results_goals_home
print "away goals:" + shots_results_goals_away
print "home on target:" + shots_results_ontarget_home
print "away on target:" + shots_results_ontarget_away
print "home off target:" + shots_results_offtarget_home
print "away off target:" + shots_results_offtarget_away
print "home woodwork:" + shots_results_woodwork_home
print "away woodwork:" + shots_results_woodwork_away
print "home blocked:" + shots_results_blocked_home
print "away blocked:" + shots_results_blocked_away
print "home own goals:" + shots_results_own_home
print "away own goals:" + shots_results_own_away
browser.quit()
