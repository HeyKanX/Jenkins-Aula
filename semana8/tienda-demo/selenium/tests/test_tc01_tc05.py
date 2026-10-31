"""Pruebas de catálogo y consulta del carrito con Playwright."""
from pathlib import Path
import unittest
import sys
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from utils.driver_factory import DriverFactory
from pages.catalog_page import CatalogPage
from pages.cart_page import CartPage

BASE_URL = (Path(__file__).resolve().parents[2] / 'app' / 'tienda_demo.html').as_uri()

class TestCatalogo(unittest.TestCase):
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

    def test_tc01_agregar_un_producto(self):
        self.catalog.add_product('Laptop Pro 15')
        self.assertEqual(self.catalog.get_cart_count(), 1)

    def test_tc02_agregar_productos_diferentes(self):
        self.catalog.add_product('Laptop Pro 15')
        self.catalog.add_product('Mouse Inalámbrico')
        self.catalog.open_cart()
        self.assertTrue(self.cart.has_item('Laptop Pro 15'))
        self.assertTrue(self.cart.has_item('Mouse Inalámbrico'))

    def test_tc03_agregar_producto_repetido(self):
        self.catalog.add_product('Laptop Pro 15')
        self.catalog.add_product('Laptop Pro 15')
        self.catalog.open_cart()
        self.assertEqual(self.cart.get_quantity('Laptop Pro 15'), 2)

    def test_tc04_actualizar_contador(self):
        self.catalog.add_product('Laptop Pro 15')
        self.catalog.add_product('Mouse Inalámbrico')
        self.assertEqual(self.catalog.get_cart_count(), 2)

    def test_tc05_consultar_producto_agregado(self):
        self.catalog.add_product('Laptop Pro 15')
        self.catalog.open_cart()
        self.assertTrue(self.cart.has_item('Laptop Pro 15'))
        self.assertEqual(self.cart.get_quantity('Laptop Pro 15'), 1)
        self.assertTrue(self.cart.get_total())

if __name__ == '__main__':
    unittest.main()
