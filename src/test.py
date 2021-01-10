import unittest
from webdriver.webdriver_handler import WebdriverHandler
import os
import asyncio

class TestWebDriver(unittest.TestCase):

    def test_initialize_open_chrome(self):
        browser_instance = WebdriverHandler()
        driver = browser_instance.driver

        driver.get("http://www.python.org")

        assert "Python" in driver.title

    def test_close_driver(self):
        browser_instance = WebdriverHandler()
        driver = browser_instance.driver
        driver.close()
        # Need to define a good assertion

    #def test_get_tweet_data(self):
        # It's a bit hard to test just the get_tweet_data method right now, 
        # because I first need to get define a "card" fixture


if __name__ == '__main__':
    unittest.main()