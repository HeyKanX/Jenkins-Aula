import os
from pathlib import Path
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class BasePage:
    def __init__(self, driver): self.driver=driver; self.wait=WebDriverWait(driver,10)
    def open(self, url=None):
        if url is None: url=(Path(__file__).resolve().parents[2]/'app'/'tienda_demo.html').as_uri()
        url = os.getenv("TIENDA_DEMO_URL", url)
        self.driver.get(url)
    def find(self, locator): return self.wait.until(EC.presence_of_element_located(locator))
    def click(self, locator): self.wait.until(EC.element_to_be_clickable(locator)).click()
    def fill(self, locator, value):
        el=self.find(locator); el.clear(); el.send_keys(value)
