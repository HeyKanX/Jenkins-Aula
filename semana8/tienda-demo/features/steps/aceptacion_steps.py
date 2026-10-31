"""Pasos Behave exclusivos de aceptacion.feature."""
from pathlib import Path
import re
from behave import given, when, then
from selenium.webdriver.common.by import By
from utils.driver_factory import DriverFactory

BASE_URL = (Path(__file__).resolve().parents[2] / "app" / "tienda_demo.html").as_uri()

def agregar_producto(context, nombre):
    for tarjeta in context.driver.find_elements(By.CSS_SELECTOR, ".tarjeta-producto"):
        if nombre in tarjeta.text:
            tarjeta.find_element(By.CSS_SELECTOR, ".btn-agregar").click()
            return
    raise AssertionError(f"Producto '{nombre}' no encontrado")

def buscar_fila(context, nombre):
    for fila in context.driver.find_elements(By.CSS_SELECTOR, ".item-carrito"):
        if nombre in fila.text:
            return fila
    return None

def abrir_checkout(context):
    context.driver.find_element(By.ID, "btn-abrir-carrito").click()
    context.driver.find_element(By.ID, "btn-ir-checkout").click()

def completar_datos(context):
    datos = {"campo-nombre":"María López", "campo-email":"maria@correo.com",
             "campo-direccion":"Jr. 9 de Octubre 456", "campo-ciudad":"Lima",
             "campo-telefono":"987654321"}
    for campo, valor in datos.items():
        context.driver.find_element(By.ID, campo).send_keys(valor)

def numero(texto):
    return float(re.sub(r"[^0-9.]", "", texto))

@given("[aceptacion] estoy en el catálogo de TiendaDemo")
def step_catalogo_aceptacion(context):
    context.driver = DriverFactory.create_chrome()
    context.driver.get(BASE_URL)

@given("[aceptacion] estoy en checkout con un producto")
def step_checkout_con_producto(context):
    agregar_producto(context, "Laptop Pro 15")
    abrir_checkout(context)

@given("[aceptacion] tengo dos productos diferentes en el carrito")
def step_dos_productos(context):
    agregar_producto(context, "Laptop Pro 15")
    agregar_producto(context, "Mouse Inalámbrico")

@given("[aceptacion] procedo al checkout")
@when("[aceptacion] procedo al checkout")
def step_proceder_checkout(context):
    vista = context.driver.find_element(By.ID, "vista-carrito")
    if "activa" not in vista.get_attribute("class"):
        context.driver.find_element(By.ID, "btn-abrir-carrito").click()
    context.driver.find_element(By.ID, "btn-ir-checkout").click()

@when('[aceptacion] agrego "{producto}" al carrito')
def step_agregar(context, producto):
    agregar_producto(context, producto)

@when("[aceptacion] abro el carrito")
def step_abrir_carrito(context):
    context.driver.find_element(By.ID, "btn-abrir-carrito").click()

@when('[aceptacion] aplico el cupón "{cupon}"')
def step_aplicar_cupon(context, cupon):
    context.driver.find_element(By.ID, "input-cupon").send_keys(cupon)
    context.driver.find_element(By.ID, "btn-aplicar-cupon").click()

@when("[aceptacion] completo los datos válidos y confirmo la compra")
def step_comprar(context):
    completar_datos(context)
    context.driver.find_element(By.ID, "btn-confirmar-pago").click()

@when('[aceptacion] confirmo el pago dejando vacío el campo "{nombre}"')
def step_pago_incompleto(context, nombre):
    completar_datos(context)
    campo_id = {"nombre":"campo-nombre", "correo":"campo-email",
                "teléfono":"campo-telefono", "dirección":"campo-direccion"}[nombre]
    campo = context.driver.find_element(By.ID, campo_id)
    campo.clear()
    context.driver.find_element(By.ID, "btn-confirmar-pago").click()

@then("[aceptacion] el contador del carrito es {cantidad:d}")
def step_contador(context, cantidad):
    actual = int(context.driver.find_element(By.ID, "contador-carrito").text)
    assert actual == cantidad

@then('[aceptacion] veo el producto "{producto}" en el carrito')
def step_producto_carrito(context, producto):
    if not buscar_fila(context, producto):
        context.driver.find_element(By.ID, "btn-abrir-carrito").click()
    assert buscar_fila(context, producto)

@then("[aceptacion] veo los dos productos diferentes en el carrito")
def step_dos_productos_carrito(context):
    assert buscar_fila(context, "Laptop Pro 15")
    assert buscar_fila(context, "Mouse Inalámbrico")

@then("[aceptacion] el subtotal del carrito es S/ {esperado:f}")
def step_subtotal(context, esperado):
    subtotal = numero(context.driver.find_element(By.ID, "valor-subtotal").text)
    assert abs(subtotal - esperado) < 0.01

@then("[aceptacion] veo el mensaje de cupón aplicado")
def step_cupon_aplicado(context):
    mensaje = context.driver.find_element(By.ID, "msg-cupon").text
    assert "DESCUENTO10" in mensaje and "aplicado" in mensaje.lower()

@then("[aceptacion] veo el error del campo \"dirección\"")
def step_error_direccion(context):
    assert context.driver.find_element(By.ID, "error-direccion").is_displayed()

@then("[aceptacion] la compra no se confirma")
def step_sin_confirmacion(context):
    assert not context.driver.find_elements(By.ID, "confirmacion-card")

@then("[aceptacion] veo la pantalla de confirmación")
def step_confirmacion(context):
    mensaje = context.driver.find_element(By.ID, "msg-confirmacion").text
    assert "Compra realizada con éxito" in mensaje

@then("[aceptacion] veo el número de orden")
def step_numero_orden(context):
    assert context.driver.find_element(By.ID, "numero-orden").text.strip()

@then("[aceptacion] no se ofrece proceder al pago")
def step_checkout_vacio(context):
    assert context.driver.find_elements(By.ID, "carrito-vacio")
    assert not context.driver.find_elements(By.ID, "btn-ir-checkout")

@then("[aceptacion] el total corresponde a un descuento del 10 por ciento")
def step_total_descuento(context):
    subtotal = numero(context.driver.find_element(By.ID, "valor-subtotal").text)
    total = numero(context.driver.find_element(By.ID, "valor-total").text)
    assert abs(total - subtotal * 0.90) < 0.02

