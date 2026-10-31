"""Pruebas Playwright de aceptación, total y casos negativos adicionales."""
from pathlib import Path
import re
import unittest
import sys
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from playwright.sync_api import sync_playwright
from pages.catalog_page import CatalogPage
from pages.cart_page import CartPage
from pages.checkout_page import CheckoutPage
from pages.confirmation_page import ConfirmationPage

BASE_URL = (Path(__file__).resolve().parents[2] / 'app' / 'tienda_demo.html').as_uri()
CUSTOMER = ('Ana Pérez', 'ana@example.com', 'Av. Lima 123', 'Lima', '987654321')

class TestAceptacion(unittest.TestCase):
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
        self.checkout = CheckoutPage(self.page)
        self.confirmation = ConfirmationPage(self.page)
        self.catalog.open(BASE_URL)

    def tearDown(self):
        self.context.close()

    @staticmethod
    def _monto(precio):
        return float(re.sub(r'[^0-9.]', '', precio))

    def _checkout_valid(self):
        self.catalog.add_product('Laptop Pro 15')
        self.catalog.open_cart()
        self.cart.proceed_to_checkout()
        self.checkout.fill_customer(*CUSTOMER)
        self.checkout.confirm_purchase()

    def test_tc32_agregar_producto_como_usuario(self):
        self.catalog.add_product('Laptop Pro 15')
        self.assertEqual(self.catalog.get_cart_count(), 1)

    def test_tc33_resumen_carrito(self):
        self.catalog.add_product('Laptop Pro 15')
        self.catalog.open_cart()
        self.assertTrue(self.cart.has_item('Laptop Pro 15'))
        self.assertIn('2,499.00', self.cart.get_subtotal())

    def test_tc34_aplicar_cupon_valido_como_usuario(self):
        self.catalog.add_product('Laptop Pro 15')
        self.catalog.open_cart()
        subtotal = self._monto(self.cart.get_subtotal())
        self.cart.apply_coupon('DESCUENTO10')
        self.assertIn('DESCUENTO10', self.cart.get_coupon_message())
        self.assertAlmostEqual(self._monto(self.cart.get_total()), subtotal * 0.90, delta=0.01)

    def test_tc35_confirmar_compra(self):
        self._checkout_valid()
        self.assertTrue(self.confirmation.is_visible())
        self.assertIn('Compra realizada con éxito', self.confirmation.get_message())

    def test_tc36_validar_nombre_vacio(self):
        self.catalog.add_product('Laptop Pro 15')
        self.catalog.open_cart()
        self.cart.proceed_to_checkout()
        self.checkout.fill_customer('', *CUSTOMER[1:])
        self.checkout.confirm_purchase()
        self.assertTrue(self.checkout.error_is_visible('error-nombre'))
        self.assertFalse(self.confirmation.is_visible())

    def test_tc37_confirmacion_con_orden(self):
        self._checkout_valid()
        self.assertTrue(self.confirmation.is_visible())
        self.assertTrue(self.confirmation.get_order_number())

    def test_tc38_compra_de_varios_productos(self):
        self.catalog.add_product('Laptop Pro 15')
        self.catalog.add_product('Mouse Inalámbrico')
        self.catalog.open_cart()
        self.assertTrue(self.cart.has_item('Laptop Pro 15'))
        self.assertTrue(self.cart.has_item('Mouse Inalámbrico'))
        self.cart.proceed_to_checkout()
        self.checkout.fill_customer(*CUSTOMER)
        self.checkout.confirm_purchase()
        self.assertTrue(self.confirmation.is_visible())

    def test_tc39_carrito_vacio(self):
        self.catalog.open_cart()
        self.assertTrue(self.cart.is_empty())
        self.assertFalse(self.cart.has_checkout_button())

    def test_tc40_total_con_descuento(self):
        self.catalog.add_product('Laptop Pro 15')
        self.catalog.open_cart()
        subtotal = self._monto(self.cart.get_subtotal())
        self.cart.apply_coupon('DESCUENTO10')
        self.assertIn('DESCUENTO10', self.cart.get_coupon_message())
        self.assertAlmostEqual(self._monto(self.cart.get_total()), subtotal * 0.90, delta=0.01)

    def test_tc41_compra_con_descuento(self):
        self.catalog.add_product('Laptop Pro 15')
        self.catalog.open_cart()
        subtotal = self._monto(self.cart.get_subtotal())
        self.cart.apply_coupon('DESCUENTO10')
        self.assertAlmostEqual(self._monto(self.cart.get_total()), subtotal * 0.90, delta=0.01)
        self.cart.proceed_to_checkout()
        self.checkout.fill_customer(*CUSTOMER)
        self.checkout.confirm_purchase()
        self.assertTrue(self.confirmation.is_visible())
        self.assertTrue(self.confirmation.get_order_number())

if __name__ == '__main__':
    unittest.main()
