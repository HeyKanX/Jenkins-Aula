"""Pruebas Selenium para cantidades, eliminación y subtotal."""
from pathlib import Path
import unittest
from unittest import skip
import sys
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from utils.driver_factory import DriverFactory
from pages.catalog_page import CatalogPage
from pages.cart_page import CartPage

BASE_URL = (Path(__file__).resolve().parents[2] / 'app' / 'tienda_demo.html').as_uri()

class TestCarrito(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.driver = DriverFactory.create_chrome(headless=True)

    @classmethod
    def tearDownClass(cls):
        cls.driver.quit()

    def setUp(self):
        self.page = self.driver
        self.catalog = CatalogPage(self.page)
        self.cart = CartPage(self.page)
        self.catalog.open(BASE_URL)

    def _add_laptop_and_open_cart(self):
        self.catalog.add_product('Laptop Pro 15')
        self.catalog.open_cart()

    def test_tc06_aumentar_cantidad(self):
        self._add_laptop_and_open_cart()
        self.cart.increase_quantity('Laptop Pro 15')
        self.assertEqual(self.cart.get_quantity('Laptop Pro 15'), 2)

    def test_tc07_disminuir_cantidad(self):
        self.catalog.add_product('Laptop Pro 15')
        self.catalog.add_product('Laptop Pro 15')
        self.catalog.open_cart()
        self.cart.decrease_quantity('Laptop Pro 15')
        self.assertEqual(self.cart.get_quantity('Laptop Pro 15'), 1)

    def test_tc08_cantidad_cero(self):
        self._add_laptop_and_open_cart()
        self.cart.decrease_quantity('Laptop Pro 15')
        self.assertFalse(self.cart.has_item('Laptop Pro 15'), 'Al reducir a cero el producto debe retirarse del carrito')

    @skip('Ejecución manual: la interfaz de referencia no ofrece un campo editable para ingresar una cantidad negativa.')
    def test_tc09_ingresar_cantidad_negativa(self):
        self._add_laptop_and_open_cart()
        quantity = self.driver.find_element('css selector', 'input.cantidad-num')
        quantity.clear()
        quantity.send_keys('-1')
        quantity.send_keys('\t')
        self.assertNotEqual(quantity.get_attribute('value'), '-1', 'La interfaz debe rechazar la cantidad negativa')

    def test_tc10_eliminar_producto(self):
        self._add_laptop_and_open_cart()
        self.cart.remove_item('Laptop Pro 15')
        self.assertFalse(self.cart.has_item('Laptop Pro 15'))

    def test_tc11_eliminar_ultimo_producto(self):
        self._add_laptop_and_open_cart()
        self.cart.remove_item('Laptop Pro 15')
        self.assertTrue(self.cart.is_empty())

    def test_tc12_conservar_otro_producto(self):
        self.catalog.add_product('Laptop Pro 15')
        self.catalog.add_product('Mouse Inalámbrico')
        self.catalog.open_cart()
        self.cart.remove_item('Laptop Pro 15')
        self.assertFalse(self.cart.has_item('Laptop Pro 15'))
        self.assertTrue(self.cart.has_item('Mouse Inalámbrico'))

    def test_tc13_actualizar_subtotal_al_eliminar_producto(self):
        self.catalog.add_product('Laptop Pro 15')
        self.catalog.add_product('Mouse Inalámbrico')
        self.catalog.open_cart()
        subtotal_antes = self.cart.get_subtotal()
        self.assertIn('2,588.90', subtotal_antes)
        self.cart.remove_item('Laptop Pro 15')
        subtotal_despues = self.cart.get_subtotal()
        self.assertNotEqual(subtotal_despues, subtotal_antes)
        self.assertIn('89.90', subtotal_despues)

if __name__ == '__main__':
    unittest.main()
