from selenium.common.exceptions import NoSuchElementException
from selenium import webdriver
import chromedriver_autoinstaller 
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

import re

from time import sleep
import asyncio


def init_driver(headless=True, proxy=None):
        # create, initialize and return instance of web driver.  Only Chrome is supported for now.
        chromedriver_path = chromedriver_autoinstaller.install()
        options = Options()

        if headless is True:
            print("Scraping on headless mode.")
            options.add_argument('--disable-gpu')
            options.headless = True
        else:
            options.headless = False

        options.add_argument('log-level=3')

        if proxy is not None:
            options.add_argument('--proxy-server=%s' % proxy)

        prefs = {"profile.managed_default_content_settings.images": 2}
        options.add_experimental_option("prefs", prefs)

        driver = webdriver.Chrome(options=options, executable_path=chromedriver_path)
        driver.set_page_load_timeout(100)

        return driver





def get_tweet_data(card):
    """Extract data from tweet card"""
    try:
        username = card.find_element_by_xpath('.//span').text
    except:
        return

    try:
        handle = card.find_element_by_xpath('.//span[contains(text(), "@")]').text
    except:
        return

    try:
        postdate = card.find_element_by_xpath('.//time').get_attribute('datetime')
    except:
        return

    try:
        comment = card.find_element_by_xpath('.//div[2]/div[2]/div[1]').text
    except:
        comment = ""

    try:
        responding = card.find_element_by_xpath('.//div[2]/div[2]/div[2]').text
    except:
        responding = ""

    text = comment + ' ' + responding

    try:
        reply_cnt = card.find_element_by_xpath('.//div[@data-testid="reply"]').text
    except:
        reply_cnt = 0

    try:
        retweet_cnt = card.find_element_by_xpath('.//div[@data-testid="retweet"]').text
    except:
        retweet_cnt = 0

    try:
        like_cnt = card.find_element_by_xpath('.//div[@data-testid="like"]').text
    except:
        like_cnt = 0

    try:
        element = card.find_element_by_xpath('.//div[2]/div[2]//img[contains(@src, "twimg")]')
        image_link = element.get_attribute('src')
    except:
        image_link = ""

    # handle promoted tweets
    try:
        promoted = card.find_element_by_xpath('.//div[2]/div[2]/[last()]//span').text == "Promoted"
    except:
        promoted = False
    if promoted:
        return

    # get a string of all emojis contained in the tweet
    try:
        emoji_tags = card.find_elements_by_xpath('.//img[contains(@src, "emoji")]')
    except:
        return
    emoji_list = []
    for tag in emoji_tags:
        try:
            filename = tag.get_attribute('src')
            emoji = chr(int(re.search(r'svg\/([a-z0-9]+)\.svg', filename).group(1), base=16))
        except AttributeError:
            continue
        if emoji:
            emoji_list.append(emoji)
    emojis = ' '.join(emoji_list)

    # tweet url
    try:
        element = card.find_element_by_xpath('.//a[contains(@href, "/status/")]')
        tweet_url = element.get_attribute('href')
    except:
        return

    try:
        hashtags_list = re.findall(r"#(\w+)", text)
    except:
        return

    try:
        fooji_link = re.findall(r'((?<=[^a-zA-Z0-9])(?:https?\:\/\/|[a-zA-Z0-9]{1,}\.{1}|\b)(?:\w{1,}\.{1}){1,5}(?:com|info){1}(?:\/[a-zA-Z0-9]{1,})*)', text)[0]
        re.compile(r"^https?://www\.(\w+)?(facebook|twitter)\.com/[\w-]+")
    except:
        return


    tweet = (username, handle, postdate, text, emojis, reply_cnt, retweet_cnt, like_cnt, image_link, tweet_url, hashtags_list, fooji_link)
    return tweet
