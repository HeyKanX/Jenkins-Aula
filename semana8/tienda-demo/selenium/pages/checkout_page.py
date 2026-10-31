"""Page Object del formulario de compra."""
from selenium.webdriver.common.by import By
from .base_page import BasePage

class CheckoutPage(BasePage):
    def fill_customer(self, name, email, address, city, phone):
        values = {'campo-nombre': name, 'campo-email': email, 'campo-direccion': address,
                  'campo-ciudad': city, 'campo-telefono': phone}
        for field, value in values.items():
            self.fill((By.ID, field), value)

    def clear_field(self, field_id):
        element = self.find((By.ID, field_id))
        element.clear()

    def fill_surname(self, surname):
        self.fill((By.ID, 'campo-apellido'), surname)

    def confirm_purchase(self):
        self.click((By.ID, 'btn-confirmar-pago'))

    def error_is_visible(self, error_id):
        elements = self.driver.find_elements(By.ID, error_id)
        return bool(elements and elements[0].is_displayed())

    def has_surname_field(self):
        return bool(self.driver.find_elements(By.ID, 'campo-apellido'))
