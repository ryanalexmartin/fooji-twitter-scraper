import unittest
from webdriver.webdriver_handler import WebdriverHandler
import os
#import os.system("python ../utils.py") as utils #not an ideal way to handle modules but will work for now

class TestWebDriver(unittest.TestCase):

    def test_initialize_open_chrome(self):
        browser_instance = WebdriverHandler()
        driver = browser_instance.driver

        driver.get("http://www.python.org")

        assert "Python" in driver.title


if __name__ == '__main__':
    unittest.main()