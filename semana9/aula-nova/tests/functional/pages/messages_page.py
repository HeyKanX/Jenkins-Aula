from selenium.webdriver.common.by import By
from pages.base_page import BasePage


class MessagesPage(BasePage):
    NAVIGATION_LINK = (By.CSS_SELECTOR, "a[data-view='mensajes']")
    VIEW = (By.ID, "view-mensajes")
    EMPTY_MESSAGE = (By.CSS_SELECTOR, "#messages-list .empty-messages")
    NEW_MESSAGE = (By.CSS_SELECTOR, "#view-mensajes [data-open-message]")
    MESSAGE_ENTRIES = (By.CSS_SELECTOR, "#messages-list .message-entry")
    TOAST = (By.ID, "toast")

    def open_messages(self):
        self.wait_clickable(self.NAVIGATION_LINK).click()
        self.wait_visible(self.VIEW)

    def is_visible(self):
        return self.driver.find_element(*self.VIEW).is_displayed()

    def empty_text(self):
        return self.wait_visible(self.EMPTY_MESSAGE).text

    def open_new_message(self):
        self.wait_clickable(self.NEW_MESSAGE).click()

    def contains_message(self, subject, body, teacher):
        for entry in self.driver.find_elements(*self.MESSAGE_ENTRIES):
            text = entry.text
            if subject in text and body in text and teacher in text:
                return True
        return False

    def toast_text(self):
        return self.wait_visible(self.TOAST).text
