"""Pasos Behave exclusivos de cupones.feature."""
from pathlib import Path
import re
from behave import given, when, then
from selenium.webdriver.common.by import By
from utils.driver_factory import DriverFactory

BASE_URL = (Path(__file__).resolve().parents[2] / "app" / "tienda_demo.html").as_uri()

def numero(texto):
    return float(re.sub(r"[^0-9.]", "", texto))

@given("[cupones] estoy en el catálogo de TiendaDemo")
def step_catalogo_cupones(context):
    context.driver = DriverFactory.create_chrome()
    context.driver.get(BASE_URL)

@when('[cupones] agrego "{producto}" al carrito')
def step_agregar_producto(context, producto):
    for tarjeta in context.driver.find_elements(By.CSS_SELECTOR, ".tarjeta-producto"):
        if producto in tarjeta.text:
            tarjeta.find_element(By.CSS_SELECTOR, ".btn-agregar").click()
            return
    raise AssertionError(f"Producto '{producto}' no encontrado")

@when("[cupones] abro el carrito")
def step_abrir_carrito(context):
    context.driver.find_element(By.ID, "btn-abrir-carrito").click()

@when('[cupones] aplico el cupón "{cupon}"')
def step_aplicar_cupon(context, cupon):
    context.driver.find_element(By.ID, "input-cupon").send_keys(cupon)
    context.driver.find_element(By.ID, "btn-aplicar-cupon").click()

@when("[cupones] aplico un cupón vacío")
def step_aplicar_cupon_vacio(context):
    context.driver.find_element(By.ID, "btn-aplicar-cupon").click()

@when('[cupones] vuelvo a aplicar el cupón "{cupon}"')
def step_reaplicar_cupon(context, cupon):
    campo = context.driver.find_element(By.ID, "input-cupon")
    campo.clear()
    campo.send_keys(cupon)
    context.driver.find_element(By.ID, "btn-aplicar-cupon").click()

@then("[cupones] veo un aviso de cupón repetido")
def step_aviso_cupon_repetido(context):
    mensaje = context.driver.find_element(By.ID, "msg-cupon").text.lower()
    assert "ya" in mensaje or "repet" in mensaje, f"El cupón repetido no se rechazó con un aviso: {mensaje}"

@then("[cupones] veo el mensaje de cupón aplicado")
def step_mensaje_cupon_aplicado(context):
    mensaje = context.driver.find_element(By.ID, "msg-cupon").text
    assert "DESCUENTO10" in mensaje and "aplicado" in mensaje.lower(), mensaje

@then("[cupones] veo el mensaje de cupón no válido")
def step_mensaje_cupon_invalido(context):
    mensaje = context.driver.find_element(By.ID, "msg-cupon").text
    assert "no válido" in mensaje.lower(), mensaje

@then("[cupones] veo el mensaje de cupón vacío")
def step_mensaje_cupon_vacio(context):
    mensaje = context.driver.find_element(By.ID, "msg-cupon").text
    assert "Ingresa un código" in mensaje, mensaje

@then("[cupones] el total corresponde a un descuento del 10 por ciento")
def step_total_con_descuento(context):
    subtotal = numero(context.driver.find_element(By.ID, "valor-subtotal").text)
    total = numero(context.driver.find_element(By.ID, "valor-total").text)
    assert abs(total - subtotal * 0.90) < 0.02

@then("[cupones] el total es igual al subtotal")
def step_total_igual_subtotal(context):
    subtotal = numero(context.driver.find_element(By.ID, "valor-subtotal").text)
    total = numero(context.driver.find_element(By.ID, "valor-total").text)
    assert abs(total - subtotal) < 0.01

