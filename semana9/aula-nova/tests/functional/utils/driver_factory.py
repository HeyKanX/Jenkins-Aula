import os

from selenium import webdriver
from selenium.webdriver.chrome.options import Options


def create_driver():
    options = Options()
    options.add_argument("--window-size=1440,1000")

    chrome_binary = os.getenv("CHROME_BIN")
    if chrome_binary:
        options.binary_location = chrome_binary

    if os.getenv("CI", "").lower() == "true":
        options.add_argument("--headless=new")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")

    remote_url = os.getenv("SELENIUM_REMOTE_URL")
    if remote_url:
        driver = webdriver.Remote(command_executor=remote_url, options=options)
    else:
        driver = webdriver.Chrome(options=options)

    if os.getenv("CI", "").lower() != "true" and not remote_url:
        driver.maximize_window()
    return driver
