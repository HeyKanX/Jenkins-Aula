"""Page Object para el catálogo de TiendaDemo."""
from selenium.webdriver.common.by import By
from .base_page import BasePage

class CatalogPage(BasePage):
    PRODUCT_CARDS = (By.CSS_SELECTOR, '.tarjeta-producto')
    CART_COUNT = (By.ID, 'contador-carrito')
    CART_BUTTON = (By.ID, 'btn-abrir-carrito')

    def add_product(self, name):
        for card in self.driver.find_elements(*self.PRODUCT_CARDS):
            if name in card.text:
                card.find_element(By.CSS_SELECTOR, '.btn-agregar').click()
                return
        raise ValueError(f"Producto '{name}' no encontrado en el catálogo")

    def open_cart(self):
        self.click(self.CART_BUTTON)

    def get_cart_count(self):
        return int(self.find(self.CART_COUNT).text)

    def exists(self, css):
        return bool(self.driver.find_elements(By.CSS_SELECTOR, css))
