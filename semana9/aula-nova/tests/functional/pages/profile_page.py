from selenium.webdriver.common.by import By
from pages.base_page import BasePage


class ProfilePage(BasePage):
    VIEW = (By.ID, "view-perfil")
    NAME = (By.ID, "profile-name")
    CODE = (By.ID, "profile-code")
    EMAIL = (By.ID, "profile-email")
    BREADCRUMB = (By.ID, "breadcrumb-current")

    def is_visible(self):
        return self.wait_visible(self.VIEW).is_displayed()

    def name(self):
        return self.driver.find_element(*self.NAME).text

    def code(self):
        return self.driver.find_element(*self.CODE).text

    def email(self):
        return self.driver.find_element(*self.EMAIL).text

    def program(self):
        return self.driver.find_element(
            By.XPATH,
            "//span[.='Programa académico']/following-sibling::strong",
        ).text

    def breadcrumb(self):
        return self.driver.find_element(*self.BREADCRUMB).text
