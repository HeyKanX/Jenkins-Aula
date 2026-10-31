"""Page Object para la confirmación de compra."""
from .base_page import BasePage

class ConfirmationPage(BasePage):
    def is_visible(self):
        return self.exists("#confirmacion-card")

    def get_message(self):
        return self.text("#msg-confirmacion")

    def get_order_number(self):
        return self.text("#numero-orden").strip()

    def continue_shopping(self):
        self.click("#btn-seguir-comprando")

