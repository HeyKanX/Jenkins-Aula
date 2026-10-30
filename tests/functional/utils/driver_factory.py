from selenium import webdriver
from selenium.webdriver.chrome.options import Options


def create_driver():
    options = Options()
    options.add_argument("--window-size=1440,1000")

    driver = webdriver.Chrome(options=options)
    driver.maximize_window()
    return driver