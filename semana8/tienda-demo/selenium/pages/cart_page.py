"""Page Object para consulta y modificación del carrito."""
from selenium.webdriver.common.by import By
from .base_page import BasePage

class CartPage(BasePage):
    ITEM_ROWS = (By.CSS_SELECTOR, '.item-carrito')
    EMPTY_MESSAGE = (By.ID, 'carrito-vacio')
    CHECKOUT_BUTTON = (By.ID, 'btn-ir-checkout')
    COUPON_INPUT = (By.ID, 'input-cupon')
    COUPON_BUTTON = (By.ID, 'btn-aplicar-cupon')
    COUPON_MESSAGE = (By.ID, 'msg-cupon')

    def get_item_row(self, name):
        for row in self.driver.find_elements(*self.ITEM_ROWS):
            if name in row.text:
                return row
        return None

    def has_item(self, name):
        return self.get_item_row(name) is not None

    def get_quantity(self, name):
        row = self.get_item_row(name)
        return int(row.find_element(By.CSS_SELECTOR, '.cantidad-num').text) if row else 0

    def increase_quantity(self, name):
        self._row_action(name, ".btn-cantidad[data-accion='mas']")

    def decrease_quantity(self, name):
        self._row_action(name, ".btn-cantidad[data-accion='menos']")

    def remove_item(self, name):
        self._row_action(name, '.btn-eliminar')

    def _row_action(self, name, selector):
        row = self.get_item_row(name)
        if row is None:
            raise ValueError(f"Producto '{name}' no encontrado en el carrito")
        row.find_element(By.CSS_SELECTOR, selector).click()

    def is_empty(self):
        return bool(self.driver.find_elements(*self.EMPTY_MESSAGE))

    def get_subtotal(self):
        return self.driver.find_element(By.ID, 'valor-subtotal').text

    def get_total(self):
        return self.driver.find_element(By.ID, 'valor-total').text

    def apply_coupon(self, code):
        self.fill(self.COUPON_INPUT, code)
        self.click(self.COUPON_BUTTON)

    def get_coupon_message(self):
        return self.driver.find_element(*self.COUPON_MESSAGE).text

    def has_checkout_button(self):
        return bool(self.driver.find_elements(*self.CHECKOUT_BUTTON))

    def proceed_to_checkout(self):
        self.click(self.CHECKOUT_BUTTON)
