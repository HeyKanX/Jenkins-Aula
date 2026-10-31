"""Page Object para el catálogo de productos."""
from .base_page import BasePage

class CatalogPage(BasePage):
    def add_product(self, name):
        cards = self.page.locator(".tarjeta-producto")
        for index in range(cards.count()):
            card = cards.nth(index)
            if name in card.inner_text():
                card.locator(".btn-agregar").click()
                return
        raise ValueError(f"Producto '{name}' no encontrado en el catálogo")

    def open_cart(self):
        self.click("#btn-abrir-carrito")

    def get_cart_count(self):
        return int(self.text("#contador-carrito"))

