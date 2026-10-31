"""Pruebas Playwright para checkout y validación de datos."""
from pathlib import Path
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

class TestCheckout(unittest.TestCase):
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

    def _open_checkout(self):
        self.catalog.add_product('Laptop Pro 15')
        self.catalog.open_cart()
        self.cart.proceed_to_checkout()

    def _fill_valid_customer(self):
        self.checkout.fill_customer(*CUSTOMER)

    def test_tc20_carrito_vacio_sin_checkout(self):
        self.catalog.open_cart()
        self.assertTrue(self.cart.is_empty())
        self.assertFalse(self.cart.has_checkout_button())

    def test_tc21_checkout_sin_datos(self):
        self._open_checkout()
        self.checkout.confirm_purchase()
        for error_id in ('error-nombre', 'error-email', 'error-direccion', 'error-ciudad', 'error-telefono'):
            self.assertTrue(self.checkout.error_is_visible(error_id), f'Debe mostrarse {error_id}')
        self.assertFalse(self.confirmation.is_visible())

    def test_tc22_nombre_obligatorio(self):
        self._open_checkout()
        self.checkout.fill_customer('', CUSTOMER[1], CUSTOMER[2], CUSTOMER[3], CUSTOMER[4])
        self.checkout.confirm_purchase()
        self.assertTrue(self.checkout.error_is_visible('error-nombre'))
        self.assertFalse(self.confirmation.is_visible())

    def test_tc23_apellido_obligatorio(self):
        self._open_checkout()
        if not self.checkout.has_surname_field():
            self.skipTest('Ejecución manual: la interfaz de referencia no contiene un campo independiente de apellido.')
        self._fill_valid_customer()
        self.checkout.fill_surname('López')
        self.checkout.clear_field('#campo-apellido')
        self.checkout.confirm_purchase()
        self.assertTrue(self.checkout.error_is_visible('error-apellido'))

    def test_tc24_correo_obligatorio(self):
        self._open_checkout()
        self.checkout.fill_customer(CUSTOMER[0], '', *CUSTOMER[2:])
        self.checkout.confirm_purchase()
        self.assertTrue(self.checkout.error_is_visible('error-email'))
        self.assertFalse(self.confirmation.is_visible())

    def test_tc25_formato_correo(self):
        self._open_checkout()
        self.checkout.fill_customer(CUSTOMER[0], 'correo-invalido', *CUSTOMER[2:])
        self.checkout.confirm_purchase()
        self.assertTrue(self.checkout.error_is_visible('error-email'))
        self.assertFalse(self.confirmation.is_visible())

    def test_tc26_telefono_obligatorio(self):
        self._open_checkout()
        self.checkout.fill_customer(*CUSTOMER[:4], '')
        self.checkout.confirm_purchase()
        self.assertTrue(self.checkout.error_is_visible('error-telefono'))
        self.assertFalse(self.confirmation.is_visible())

    def test_tc27_direccion_obligatoria(self):
        self._open_checkout()
        self.checkout.fill_customer(CUSTOMER[0], CUSTOMER[1], '', CUSTOMER[3], CUSTOMER[4])
        self.checkout.confirm_purchase()
        self.assertTrue(self.checkout.error_is_visible('error-direccion'))
        self.assertFalse(self.confirmation.is_visible())

    def test_tc28_compra_valida(self):
        self._open_checkout()
        self._fill_valid_customer()
        self.checkout.confirm_purchase()
        self.assertTrue(self.confirmation.is_visible())
        self.assertIn('Compra realizada con éxito', self.confirmation.get_message())

    def test_tc29_compra_con_varios_productos(self):
        self.catalog.add_product('Laptop Pro 15')
        self.catalog.add_product('Mouse Inalámbrico')
        self.catalog.open_cart()
        self.assertTrue(self.cart.has_item('Laptop Pro 15'))
        self.assertTrue(self.cart.has_item('Mouse Inalámbrico'))
        self.cart.proceed_to_checkout()
        self._fill_valid_customer()
        self.checkout.confirm_purchase()
        self.assertTrue(self.confirmation.is_visible())

    def test_tc30_generar_numero_orden(self):
        self._open_checkout()
        self._fill_valid_customer()
        self.checkout.confirm_purchase()
        self.assertTrue(self.confirmation.is_visible())
        self.assertTrue(self.confirmation.get_order_number())

    def test_tc31_continuar_comprando(self):
        self._open_checkout()
        self._fill_valid_customer()
        self.checkout.confirm_purchase()
        self.confirmation.continue_shopping()
        self.assertTrue(self.catalog.exists('#grid-productos'))

if __name__ == '__main__':
    unittest.main()
