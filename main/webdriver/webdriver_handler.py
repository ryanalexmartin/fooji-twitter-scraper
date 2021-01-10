from webdriver.webdriver_utils import init_driver

class WebdriverHandler:
    driver = None
    def __init__(self):
        self.driver = init_driver()
    


