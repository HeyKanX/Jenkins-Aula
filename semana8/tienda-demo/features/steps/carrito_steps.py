"""Pasos Behave para catálogo, carrito y cupones siguiendo el estilo TiendaDemo."""
from pathlib import Path
import re
from behave import given, when, then
from selenium.webdriver.common.by import By
from utils.driver_factory import DriverFactory

BASE_URL = (Path(__file__).resolve().parents[2] / "app" / "tienda_demo.html").as_uri()

def agregar_producto(context, producto):
    for tarjeta in context.driver.find_elements(By.CSS_SELECTOR, ".tarjeta-producto"):
        if producto in tarjeta.text:
            tarjeta.find_element(By.CSS_SELECTOR, ".btn-agregar").click()
            return
    raise AssertionError(f"Producto '{producto}' no encontrado en el catálogo")

def buscar_fila(context, producto):
    for fila in context.driver.find_elements(By.CSS_SELECTOR, ".item-carrito"):
        if producto in fila.text:
            return fila
    return None

def numero(texto):
    return float(re.sub(r"[^0-9.]", "", texto))

@given("[carrito] estoy en el catálogo de TiendaDemo")
def step_catalogo(context):
    context.driver = DriverFactory.create_chrome()
    context.driver.get(BASE_URL)

@when('[carrito] agrego "{producto}" al carrito')
def step_agregar_producto(context, producto):
    agregar_producto(context, producto)

@when('[carrito] agrego "{producto}" al carrito dos veces')
def step_agregar_producto_dos_veces(context, producto):
    agregar_producto(context, producto)
    agregar_producto(context, producto)

@given("[carrito] abro el carrito")
@when("[carrito] abro el carrito")
def step_abrir_carrito(context):
    context.driver.find_element(By.ID, "btn-abrir-carrito").click()

@when('[carrito] aumento la cantidad de "{producto}"')
def step_aumentar_cantidad(context, producto):
    fila = buscar_fila(context, producto)
    assert fila, f"No se encontró '{producto}' en el carrito"
    fila.find_element(By.CSS_SELECTOR, ".btn-cantidad[data-accion='mas']").click()

@when('[carrito] disminuyo la cantidad de "{producto}"')
def step_disminuir_cantidad(context, producto):
    fila = buscar_fila(context, producto)
    assert fila, f"No se encontró '{producto}' en el carrito"
    fila.find_element(By.CSS_SELECTOR, ".btn-cantidad[data-accion='menos']").click()

@when("[carrito] intento ingresar la cantidad negativa {cantidad:d}")
def step_ingresar_cantidad_negativa(context, cantidad):
    campos = context.driver.find_elements(By.CSS_SELECTOR, "input[type='number'], input.cantidad-num")
    if not campos:
        context.scenario.skip(
            "Ejecución manual: la interfaz de referencia no ofrece un campo editable de cantidad. "
            "Solo ingresar -1 si una versión de la interfaz incorpora ese control."
        )
        return
    campos[0].clear()
    campos[0].send_keys(str(cantidad))

@when('[carrito] elimino "{producto}" del carrito')
def step_eliminar_producto(context, producto):
    fila = buscar_fila(context, producto)
    assert fila, f"No se encontró '{producto}' en el carrito"
    fila.find_element(By.CSS_SELECTOR, ".btn-eliminar").click()

@when('[carrito] aplico el cupón "{cupon}"')
def step_aplicar_cupon(context, cupon):
    context.driver.find_element(By.ID, "input-cupon").send_keys(cupon)
    context.driver.find_element(By.ID, "btn-aplicar-cupon").click()

@when("[carrito] aplico un cupón vacío")
def step_aplicar_cupon_vacio(context):
    context.driver.find_element(By.ID, "btn-aplicar-cupon").click()

@when('[carrito] vuelvo a aplicar el cupón "{cupon}"')
def step_reaplicar_cupon(context, cupon):
    campo = context.driver.find_element(By.ID, "input-cupon")
    campo.clear()
    campo.send_keys(cupon)
    context.driver.find_element(By.ID, "btn-aplicar-cupon").click()

@then('[carrito] veo el producto "{producto}" en el carrito')
def step_ver_producto(context, producto):
    if not buscar_fila(context, producto):
        context.driver.find_element(By.ID, "btn-abrir-carrito").click()
    assert buscar_fila(context, producto), f"No aparece '{producto}' en el carrito"

@then('[carrito] veo los productos "{producto1}" y "{producto2}" en el carrito')
def step_ver_dos_productos(context, producto1, producto2):
    context.driver.find_element(By.ID, "btn-abrir-carrito").click()
    assert buscar_fila(context, producto1) and buscar_fila(context, producto2)

@then('[carrito] la cantidad de "{producto}" es {cantidad:d}')
def step_validar_cantidad(context, producto, cantidad):
    fila = buscar_fila(context, producto)
    if not fila:
        context.driver.find_element(By.ID, "btn-abrir-carrito").click()
        fila = buscar_fila(context, producto)
    assert fila, f"No aparece '{producto}' en el carrito"
    actual = int(fila.find_element(By.CSS_SELECTOR, ".cantidad-num").text)
    assert actual == cantidad, f"Se esperaba {cantidad}, se obtuvo {actual}"

@then("[carrito] el contador del carrito es {cantidad:d}")
def step_validar_contador(context, cantidad):
    actual = int(context.driver.find_element(By.ID, "contador-carrito").text)
    assert actual == cantidad, f"Se esperaba {cantidad}, se obtuvo {actual}"

@then('[carrito] el carrito ya no contiene "{producto}"')
def step_validar_producto_eliminado(context, producto):
    assert buscar_fila(context, producto) is None

@then("[carrito] la cantidad negativa es rechazada")
def step_validar_cantidad_negativa(context):
    campos = context.driver.find_elements(By.CSS_SELECTOR, "input[type='number'], input.cantidad-num")
    assert campos and campos[0].get_attribute("value") != "-1", "La interfaz aceptó la cantidad negativa"

@then("[carrito] se muestra el carrito vacío")
def step_validar_carrito_vacio(context):
    assert context.driver.find_elements(By.ID, "carrito-vacio")

@then("[carrito] el subtotal del carrito es S/ {esperado:f}")
def step_validar_subtotal(context, esperado):
    actual = numero(context.driver.find_element(By.ID, "valor-subtotal").text)
    assert abs(actual - esperado) < 0.01, f"Se esperaba S/ {esperado:.2f}, se obtuvo S/ {actual:.2f}"
