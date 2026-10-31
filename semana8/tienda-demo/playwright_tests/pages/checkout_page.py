"""Page Object para validar y enviar el formulario de checkout."""
from .base_page import BasePage

class CheckoutPage(BasePage):
    def fill_customer(self, name, email, address, city, phone):
        self.fill("#campo-nombre", name)
        self.fill("#campo-email", email)
        self.fill("#campo-direccion", address)
        self.fill("#campo-ciudad", city)
        self.fill("#campo-telefono", phone)

    def clear_field(self, selector):
        self.fill(selector, "")

    def fill_surname(self, surname):
        self.fill("#campo-apellido", surname)

    def confirm_purchase(self):
        self.click("#btn-confirmar-pago")

    def error_is_visible(self, error_id):
        return self.page.locator(f"#{error_id}").is_visible()

    def has_surname_field(self):
        return self.exists("#campo-apellido")

