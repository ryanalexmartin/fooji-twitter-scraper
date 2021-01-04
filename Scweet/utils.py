from io import StringIO, BytesIO
import os
import re
from time import sleep
import chromedriver_autoinstaller
from selenium.common.exceptions import NoSuchElementException
from selenium import webdriver
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
#import requests
#import zipfile

#current_dir = pathlib.Path(__file__).parent.absolute()

"""

class OperatingSystem:
    WINDOWS = "Windows"
    LINUX = "Linux"
    MAC = "Darwin"


def download_chromedriver(version_string, operating_system: str):

    version_string_patch_strip = '.'.join(version_string.split(".")[:-1])
    zip_names = {
        OperatingSystem.MAC: "chromedriver_mac64.zip",
        OperatingSystem.WINDOWS: "chromedriver_win32.zip",
        OperatingSystem.LINUX: "chromedriver_linux64.zip"
    }

    extension = ".exe" if operating_system == OperatingSystem.WINDOWS else ""
    chromedriver_out_filename = f"chromedriver_{version_string}{extension}"
    chromedriver_path = current_dir.joinpath("drivers").joinpath(chromedriver_out_filename)

    if chromedriver_path.exists():
        return chromedriver_path

    # Chromedriver not downloaded. Lets download.
    print("Dowloading driver...")
    content = requests.get(f"https://chromedriver.storage.googleapis.com/LATEST_RELEASE_{version_string_patch_strip}")
    supported_version = content.text
    zip_name = zip_names[operating_system]

    zip_resp = requests.get(f"https://chromedriver.storage.googleapis.com/{supported_version}/{zip_name}")
    zip_binary = BytesIO(zip_resp.content)

    zip_file = zipfile.ZipFile(zip_binary)

    chromedriver_binary = zip_file.read(f"chromedriver{extension}")

    with open(chromedriver_path, "wb+") as chromeriver_file:
        chromeriver_file.write(chromedriver_binary)
    os.chmod(chromedriver_path, 0o777)

    return chromedriver_path

def chrome_version():
    osname = platform.system()
    if osname == OperatingSystem.MAC:
        install_paths = [
            "/Applications/Google\ Chrome.app/Contents/MacOS/Google\ Chrome"
        ]
    elif osname == OperatingSystem.WINDOWS:
        install_paths = [
            "C:\Program Files (x86)\Google\Chrome\Application\chrome.exe"
        ]
    elif osname == OperatingSystem.LINUX:
        install_paths = [
            "/usr/bin/google-chrome",
            "/usr/bin/google-chrome-stable"
        ]
    else:
        raise NotImplemented(f"Unknown OS '{osname}'")

    version_strings = [os.popen(f"{ip} --version").read().strip('Google Chrome ').strip() for ip in install_paths]
    version_strings = list(sorted(filter(None, version_strings)))

    if len(version_strings) == 0:
        raise RuntimeError("Could not find Chrome installed on this system")

    return version_strings.pop()

"""
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

    text = comment + responding

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

    tweet = (username, handle, postdate, text, emojis, reply_cnt, retweet_cnt, like_cnt, image_link, tweet_url)
    return tweet


def init_driver(navig="chrome", headless=True, proxy=None):
    # create instance of web driver

    if navig == "chrome":

        #version = chrome_version()
        #chromedriver_path = download_chromedriver(version, platform.system())

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
    elif navig == "edge":
        browser_path = 'drivers/msedgedriver.exe'
        options = EdgeOptions()
        if proxy is not None:
            options.add_argument('--proxy-server=%s' % proxy)
        if headless:
            options.headless = True
            options.use_chromium = False
        else:
            options.headless = False
            options.use_chromium = True
        options.add_argument('log-level=3')
        driver = Edge(options=options, executable_path=browser_path)
        return driver


def log_search_page(driver, start_date, end_date, lang, display_type, words, to_account, from_account):
    """ Search for this query between start_date and end_date"""

    # req='%20OR%20'.join(words)
    from_account = "(from%3A" + from_account + ")%20" if from_account is not None else ""
    to_account = "(to%3A" + to_account + ")%20" if to_account is not None else ""

    if words is not None:
        words = str(words).split("//")
        words = "(" + str('%20OR%20'.join(words)) + ")%20"
    else:
        words = ""

    if lang is not None:
        lang = 'lang%3A' + lang
    else:
        lang = ""

    end_date = "until%3A" + end_date + "%20"
    start_date = "since%3A" + start_date + "%20"

    # to_from = str('%20'.join([from_account,to_account]))+"%20"

    driver.get(
        'https://twitter.com/search?q=' + words + from_account + to_account + end_date + start_date + lang + '&src=typed_query')

    sleep(1)

    # navigate to historical 'Top' or 'Latest' tab
    try:
        driver.find_element_by_link_text(display_type).click()
    except:
        print("Latest Button doesnt exist.")


def get_last_date_from_csv(path):
    df = pd.read_csv(path)
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


def keep_scroling(driver, data, writer, tweet_ids, scrolling, tweet_parsed, limit, scroll, last_position):
    """ scrolling function """

    while scrolling and tweet_parsed < limit:
        # get the card of tweets
        page_cards = driver.find_elements_by_xpath('//div[@data-testid="tweet"]')
        for card in page_cards:
            tweet = get_tweet_data(card)
            if tweet:
                # check if the tweet is unique
                tweet_id = ''.join(tweet[:-1])
                if tweet_id not in tweet_ids:
                    tweet_ids.add(tweet_id)
                    data.append(tweet)
                    last_date = str(tweet[2])
                    print("Tweet made at: " + str(last_date) + " is found.")
                    writer.writerows([tweet])
                    tweet_parsed += 1
                    if tweet_parsed >= limit:
                        break
        scroll_attempt = 0
        while True and tweet_parsed < limit:
            # check scroll position
            print("scroll", scroll)
            # sleep(1)
            driver.execute_script('window.scrollTo(0, document.body.scrollHeight);')
            scroll += 1
            sleep(1)
            curr_position = driver.execute_script("return window.pageYOffset;")
            if last_position == curr_position:
                scroll_attempt += 1

                # end of scroll region
                if scroll_attempt >= 2:
                    scrolling = False
                    break
                else:
                    sleep(1)  # attempt another scroll
            else:
                last_position = curr_position
                break
    return driver, data, writer, tweet_ids, scrolling, tweet_parsed, scroll, last_position


def get_follow(user, headless, follow=None, verbose=1, wait=2):
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

