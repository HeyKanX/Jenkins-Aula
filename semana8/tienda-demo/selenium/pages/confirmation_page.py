"""Page Object de la confirmación de compra."""
from selenium.webdriver.common.by import By
from .base_page import BasePage

class ConfirmationPage(BasePage):
    def is_visible(self):
        elements = self.driver.find_elements(By.ID, 'confirmacion-card')
        return bool(elements and elements[0].is_displayed())

    def get_message(self):
        return self.driver.find_element(By.ID, 'msg-confirmacion').text

    def get_order_number(self):
        return self.driver.find_element(By.ID, 'numero-orden').text.strip()

    def continue_shopping(self):
        self.click((By.ID, 'btn-seguir-comprando'))
