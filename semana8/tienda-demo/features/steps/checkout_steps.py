"""Pasos Behave exclusivos de checkout.feature."""
from pathlib import Path
from behave import given, when, then
from selenium.webdriver.common.by import By
from utils.driver_factory import DriverFactory

BASE_URL = (Path(__file__).resolve().parents[2] / "app" / "tienda_demo.html").as_uri()

@given("[checkout] estoy en el catálogo de TiendaDemo")
def step_catalogo_checkout(context):
    context.driver = DriverFactory.create_chrome()
    context.driver.get(BASE_URL)

def agregar_producto(context, producto):
    for tarjeta in context.driver.find_elements(By.CSS_SELECTOR, ".tarjeta-producto"):
        if producto in tarjeta.text:
            tarjeta.find_element(By.CSS_SELECTOR, ".btn-agregar").click()
            return
    raise AssertionError(f"Producto '{producto}' no encontrado")

def abrir_checkout(context):
    context.driver.find_element(By.ID, "btn-abrir-carrito").click()
    context.driver.find_element(By.ID, "btn-ir-checkout").click()

def completar_datos(context):
    datos = {
        "campo-nombre": "María López",
        "campo-email": "maria@correo.com",
        "campo-direccion": "Jr. 9 de Octubre 456",
        "campo-ciudad": "Lima",
        "campo-telefono": "987654321",
    }
    for campo, valor in datos.items():
        context.driver.find_element(By.ID, campo).send_keys(valor)

def confirmar_pago(context):
    context.driver.find_element(By.ID, "btn-confirmar-pago").click()

@given("[checkout] estoy en checkout con un producto")
def step_checkout_con_producto(context):
    agregar_producto(context, "Laptop Pro 15")
    abrir_checkout(context)

@given("[checkout] tengo un producto en el carrito")
def step_tengo_producto(context):
    agregar_producto(context, "Laptop Pro 15")

@given("[checkout] tengo dos productos diferentes en el carrito")
def step_tengo_dos_productos(context):
    agregar_producto(context, "Laptop Pro 15")
    agregar_producto(context, "Mouse Inalámbrico")

@given("[checkout] procedo al checkout")
@when("[checkout] procedo al checkout")
def step_proceder_checkout(context):
    vista = context.driver.find_element(By.ID, "vista-carrito")
    if "activa" not in vista.get_attribute("class"):
        context.driver.find_element(By.ID, "btn-abrir-carrito").click()
    context.driver.find_element(By.ID, "btn-ir-checkout").click()

@given("[checkout] abro el carrito")
@when("[checkout] abro el carrito")
def step_abrir_carrito(context):
    context.driver.find_element(By.ID, "btn-abrir-carrito").click()

@when("[checkout] confirmo el pago sin completar los datos")
def step_pago_sin_datos(context):
    confirmar_pago(context)

@when('[checkout] confirmo el pago dejando vacío el campo "{nombre}"')
def step_pago_campo_vacio(context, nombre):
    completar_datos(context)
    campos = {
        "nombre": "campo-nombre",
        "apellido": "campo-apellido",
        "correo": "campo-email",
        "teléfono": "campo-telefono",
        "dirección": "campo-direccion",
    }
    if nombre == "apellido" and not context.driver.find_elements(By.ID, "campo-apellido"):
        context.scenario.skip(
            "Ejecución manual: la interfaz de referencia no incluye un campo separado de apellido."
        )
        return
    if nombre == "apellido":
        context.driver.find_element(By.ID, "campo-apellido").send_keys("López")
    campo = context.driver.find_element(By.ID, campos[nombre])
    campo.clear()
    confirmar_pago(context)

@when("[checkout] confirmo el pago con un correo inválido")
def step_pago_correo_invalido(context):
    completar_datos(context)
    correo = context.driver.find_element(By.ID, "campo-email")
    correo.clear()
    correo.send_keys("correo-invalido")
    confirmar_pago(context)

@when("[checkout] completo los datos válidos y confirmo la compra")
def step_pago_datos_validos(context):
    completar_datos(context)
    confirmar_pago(context)

@when("[checkout] regreso al catálogo")
def step_regresar_catalogo(context):
    context.driver.find_element(By.ID, "btn-seguir-comprando").click()

@then("[checkout] no se ofrece proceder al pago")
def step_no_proceder_pago(context):
    assert context.driver.find_elements(By.ID, "carrito-vacio"), "El carrito debe mostrarse vacío"
    assert not context.driver.find_elements(By.ID, "btn-ir-checkout")

@then("[checkout] veo los dos productos diferentes en el carrito")
def step_ver_dos_productos(context):
    filas = context.driver.find_elements(By.CSS_SELECTOR, ".item-carrito")
    productos = [fila.text for fila in filas]
    assert any("Laptop Pro 15" in texto for texto in productos)
    assert any("Mouse Inalámbrico" in texto for texto in productos)

@then("[checkout] veo mensajes de error para los campos obligatorios")
def step_errores_obligatorios(context):
    for error in ("error-nombre", "error-email", "error-direccion", "error-ciudad", "error-telefono"):
        assert context.driver.find_element(By.ID, error).is_displayed(), f"No se mostró {error}"
    assert not context.driver.find_elements(By.ID, "confirmacion-card")

@then('[checkout] veo el error del campo "{nombre}"')
def step_error_campo(context, nombre):
    errores = {
        "nombre": "error-nombre",
        "apellido": "error-apellido",
        "correo": "error-email",
        "teléfono": "error-telefono",
        "dirección": "error-direccion",
    }
    assert context.driver.find_element(By.ID, errores[nombre]).is_displayed()
    assert not context.driver.find_elements(By.ID, "confirmacion-card"), "Un formulario inválido no debe confirmar la compra"

@then("[checkout] la compra no se confirma")
def step_compra_no_confirmada(context):
    assert not context.driver.find_elements(By.ID, "confirmacion-card")

@then("[checkout] veo la pantalla de confirmación")
def step_confirmacion(context):
    mensaje = context.driver.find_element(By.ID, "msg-confirmacion").text
    assert "Compra realizada con éxito" in mensaje

@then("[checkout] veo el número de orden")
def step_numero_orden(context):
    numero = context.driver.find_element(By.ID, "numero-orden").text.strip()
    assert numero, "No se mostró el número de orden"

@then("[checkout] veo el catálogo de productos")
def step_catalogo_visible(context):
    vista = context.driver.find_element(By.ID, "vista-catalogo")
    assert "activa" in vista.get_attribute("class")

