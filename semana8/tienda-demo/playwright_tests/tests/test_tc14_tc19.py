"""Pruebas Playwright de aplicación y validación de cupones."""
from pathlib import Path
import re
import unittest
import sys
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from playwright.sync_api import sync_playwright
from pages.catalog_page import CatalogPage
from pages.cart_page import CartPage

BASE_URL = (Path(__file__).resolve().parents[2] / 'app' / 'tienda_demo.html').as_uri()

class TestCupones(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.playwright = sync_playwright().start()
        cls.browser = cls.playwright.chromium.launch(headless=True)

    @classmethod
    def tearDownClass(cls):
        cls.browser.close()
        cls.playwright.stop()

    def setUp(self):
        self.context = self.browser.new_context()
        self.page = self.context.new_page()
        self.catalog = CatalogPage(self.page)
        self.cart = CartPage(self.page)
        self.catalog.open(BASE_URL)
        self.catalog.add_product('Laptop Pro 15')
        self.catalog.open_cart()

    def tearDown(self):
        self.context.close()

    @staticmethod
    def _monto(precio):
        return float(re.sub(r'[^0-9.]', '', precio))

    def test_tc14_aceptar_cupon_valido(self):
        subtotal = self._monto(self.cart.get_subtotal())
        self.cart.apply_coupon('DESCUENTO10')
        self.assertIn('DESCUENTO10', self.cart.get_coupon_message())
        total = self._monto(self.cart.get_total())
        self.assertAlmostEqual(total, subtotal * 0.90, delta=0.01)

    def test_tc15_rechazar_cupon_invalido(self):
        before = self.cart.get_total()
        self.cart.apply_coupon('INVALIDO')
        self.assertEqual(self.cart.get_total(), before)
        self.assertIn('no válido', self.cart.get_coupon_message().lower())

    def test_tc16_rechazar_cupon_vacio(self):
        total_antes = self.cart.get_total()
        self.cart.apply_coupon('')
        self.assertIn('Ingresa un código', self.cart.get_coupon_message())
        self.assertEqual(self.cart.get_total(), total_antes)

    def test_tc17_cupon_repetido(self):
        subtotal = self._monto(self.cart.get_subtotal())
        self.cart.apply_coupon('DESCUENTO10')
        total_primera_aplicacion = self._monto(self.cart.get_total())
        self.cart.apply_coupon('DESCUENTO10')
        total_segunda_aplicacion = self._monto(self.cart.get_total())
        self.assertAlmostEqual(total_primera_aplicacion, subtotal * 0.90, delta=0.01)
        self.assertAlmostEqual(total_segunda_aplicacion, total_primera_aplicacion, delta=0.01)
        mensaje = self.cart.get_coupon_message().lower()
        self.assertTrue('ya' in mensaje or 'repet' in mensaje,
                        f'El cupón repetido debe rechazarse con un aviso; mensaje recibido: {mensaje}')

    def test_tc18_calcular_descuento_diez_por_ciento(self):
        subtotal = self._monto(self.cart.get_subtotal())
        self.cart.apply_coupon('DESCUENTO10')
        self.assertIn('DESCUENTO10', self.cart.get_coupon_message())
        total = self._monto(self.cart.get_total())
        self.assertAlmostEqual(total, subtotal * 0.90, delta=0.01)

    def test_tc19_sin_cupon_total_igual_subtotal(self):
        self.assertEqual(self.cart.get_total(), self.cart.get_subtotal())

if __name__ == '__main__':
    unittest.main()
