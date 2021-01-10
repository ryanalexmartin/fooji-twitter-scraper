from io import StringIO, BytesIO
import os
import re
from time import sleep
from selenium.common.exceptions import NoSuchElementException
from selenium import webdriver
import chromedriver_autoinstaller 
from selenium.webdriver.chrome.options import Options
import datetime
import pandas as pd
import platform
from selenium.webdriver.common.keys import Keys
#import pathlib



from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

import const
import config
import asyncio
import discord



def get_search_page(driver, lang, display_type, words, to_account, from_account, hashtag):
    # Search for this query between start_date and end_date

    # req='%20OR%20'.join(words)
    from_account = "(from%3A" + from_account + ")%20" if from_account is not None else ""
    to_account = "(to%3A" + to_account + ")%20" if to_account is not None else ""
    hash_tags = "(%23"+hashtag+")%20" if hashtag is not None else ""

    if words is not None:
        words = str(words).split("//")
        words = "(" + str('%20OR%20'.join(words)) + ")%20"
    else:
        words = ""

    if lang is not None:
        lang = 'lang%3A' + lang
    else:
        lang = ""

    # end_date = "until%3A" + end_date + "%20"
    # start_date = "since%3A" + start_date + "%20"

    # to_from = str('%20'.join([from_account,to_account]))+"%20"

    driver.get(
        'https://twitter.com/search?q=' + words + from_account + to_account + hash_tags + lang + '&src=typed_query')

    sleep(1)

    # navigate to historical 'Top' or 'Latest' tab
    try:
        driver.find_element_by_link_text(display_type).click()
    except:
        print("\'Latest\' button could not be found.")


# def log_search_page(driver, lang, display_type, words, to_account, from_account):
#     """ Search for this query between start_date and end_date"""

#     # req='%20OR%20'.join(words)
#     from_account = "(from%3A" + from_account + ")%20" if from_account is not None else ""
#     to_account = "(to%3A" + to_account + ")%20" if to_account is not None else ""

#     if words is not None:
#         words = str(words).split("//")
#         words = "(" + str('%20OR%20'.join(words)) + ")%20"
#     else:
#         words = ""

#     if lang is not None:
#         lang = 'lang%3A' + lang
#     else:
#         lang = ""

#     # to_from = str('%20'.join([from_account,to_account]))+"%20"

#     driver.get(
#         'https://twitter.com/search?q=' + words + from_account + to_account + lang + '&src=typed_query')

#     sleep(1)

#     # navigate to historical 'Top' or 'Latest' tab
#     try:
#         driver.find_element_by_link_text(display_type).click()
#     except:
#         print("Latest Button doesnt exist.")


def get_last_date_from_csv(path):
    df = pd.read_csv(path, header=[0])
    df.columns= ['UserScreenName', 'UserName', 'Timestamp', 'Text', 'Emojis', 'Comments', 'Likes', 'Retweets',
                  'Image link', 'Tweet URL', 'Hashtags', 'fooji_link']
    return datetime.datetime.strftime(max(pd.to_datetime(df["Timestamp"])), '%Y-%m-%dT%H:%M:%S.000Z')


def log_in(driver, timeout=10):

	username=const.USERNAME
	password=const.PASSWORD

	driver.get('https://www.twitter.com/login')
	username_xpath = '//input[@name="session[username_or_email]"]'
	password_xpath = '//input[@name="session[password]"]'

	username_el = WebDriverWait(driver, timeout).until(EC.presence_of_element_located((By.XPATH, username_xpath)))
	password_el = WebDriverWait(driver, timeout).until(EC.presence_of_element_located((By.XPATH, password_xpath)))

	username_el.send_keys(username)
	password_el.send_keys(password)
	password_el.send_keys(Keys.RETURN)



def get_follow(user, headless, follow=None, verbose=1, wait=10):
    driver = init_driver(headless=headless)
    sleep(wait)
    log_in(driver)
    sleep(wait)
    # log_user_page(user,driver)
    driver.get('https://twitter.com/' + user)

    sleep(wait)

    driver.find_element_by_xpath('//a[contains(@href,"/' + user + '/' + follow + '")]/span[1]/span[1]').click()
    sleep(wait)

    if check_exists_by_link_text("Log in", driver):
        login = driver.find_element_by_link_text("Log in")
        sleep(wait)
        driver.execute_script("arguments[0].click();", login)
        sleep(wait)
        driver.get('https://twitter.com/' + user)
        sleep(wait)
        driver.find_element_by_xpath('//a[contains(@href,"/' + user + '/' + follow + '")]/span[1]/span[1]').click()
        sleep(wait)

    scrolling = True
    last_position = driver.execute_script("return window.pageYOffset;")
    follows_elem = []

    while scrolling:
        # get the card of followings
        page_cards = driver.find_elements_by_xpath('//div[contains(@data-testid,"UserCell")]')
        for card in page_cards:
            element = card.find_element_by_xpath('.//div[1]/div[1]/div[1]//a[1]')
            follow_elem = element.get_attribute('href')
            follows_elem.append(follow_elem)
            if verbose:
                print(follow_elem)
        print("Found " + str(len(follows_elem)) + " " + follow)
        scroll_attempt = 0
        while True:
            sleep(wait)
            driver.execute_script('window.scrollTo(0, document.body.scrollHeight);')
            sleep(wait)
            curr_position = driver.execute_script("return window.pageYOffset;")
            if last_position == curr_position:
                scroll_attempt += 1

                # end of scroll region
                if scroll_attempt >= 3:
                    scrolling = False
                    return follows_elem
                else:
                    sleep(wait)  # attempt another scroll
            else:
                last_position = curr_position
                break


def check_exists_by_link_text(text, driver):
    try:
        driver.find_element_by_link_text(text)
    except NoSuchElementException:
        return False
    return True

