from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from pages.base_page import BasePage


class MessageDialogPage(BasePage):
    DIALOG = (By.ID, "message-dialog")
    COURSE = (By.ID, "message-course")
    SUBJECT = (By.ID, "message-subject")
    BODY = (By.ID, "message-body")
    SEND = (By.ID, "send-message")
    CANCEL = (By.ID, "cancel-dialog")
    FEEDBACK = (By.ID, "form-feedback")

    def is_open(self):
        return self.wait_visible(self.DIALOG).is_displayed()

    def select_course(self, course_id):
        Select(self.driver.find_element(*self.COURSE)).select_by_value(course_id)

    def fill_subject(self, subject):
        field = self.driver.find_element(*self.SUBJECT)
        field.clear()
        field.send_keys(subject)

    def fill_body(self, body):
        field = self.driver.find_element(*self.BODY)
        field.clear()
        field.send_keys(body)

    def send(self):
        self.wait_clickable(self.SEND).click()

    def cancel(self):
        self.wait_clickable(self.CANCEL).click()

    def feedback(self):
        return self.wait.until(
            lambda driver: driver.find_element(*self.FEEDBACK).text
        )

    def is_closed(self):
        return not self.driver.find_element(*self.DIALOG).is_displayed()
