from selenium.common.exceptions import NoSuchElementException
from selenium import webdriver
import chromedriver_autoinstaller 
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

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
