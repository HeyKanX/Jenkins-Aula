"""Page Object para consultar y modificar el carrito."""
from .base_page import BasePage

class CartPage(BasePage):
    def get_item_row(self, name):
        row = self.page.locator(".item-carrito").filter(has_text=name)
        return row.first if row.count() else None

    def has_item(self, name):
        return self.get_item_row(name) is not None

    def get_quantity(self, name):
        row = self.get_item_row(name)
        return int(row.locator(".cantidad-num").inner_text()) if row else 0

    def increase_quantity(self, name):
        row = self.get_item_row(name)
        if row is None:
            raise ValueError(f"Producto '{name}' no encontrado en el carrito")
        row.locator(".btn-cantidad[data-accion='mas']").click()

    def decrease_quantity(self, name):
        row = self.get_item_row(name)
        if row is None:
            raise ValueError(f"Producto '{name}' no encontrado en el carrito")
        row.locator(".btn-cantidad[data-accion='menos']").click()

    def remove_item(self, name):
        row = self.get_item_row(name)
        if row is None:
            raise ValueError(f"Producto '{name}' no encontrado en el carrito")
        row.locator(".btn-eliminar").click()

    def is_empty(self):
        return self.exists("#carrito-vacio")

    def get_subtotal(self):
        return self.text("#valor-subtotal")

    def get_total(self):
        return self.text("#valor-total")

    def apply_coupon(self, code):
        self.fill("#input-cupon", code)
        self.click("#btn-aplicar-cupon")

    def get_coupon_message(self):
        return self.text("#msg-cupon")

    def has_checkout_button(self):
        return self.exists("#btn-ir-checkout")

    def proceed_to_checkout(self):
        self.click("#btn-ir-checkout")

