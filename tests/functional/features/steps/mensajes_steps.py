from behave import then, when
from pages.home_page import HomePage
from pages.message_dialog_page import MessageDialogPage
from pages.messages_page import MessagesPage


VALID_SUBJECT = "Consulta de práctica"
VALID_BODY = "¿Podría explicar el ejercicio número tres?"
VALID_COURSE = "calc-201"


@when('selecciono "Mensajes" en el menú')
def step_open_messages(context):
    context.messages_page = MessagesPage(context.driver, context.base_url)
    context.messages_page.open_messages()


@when('selecciono "Escribir a un profesor"')
def step_open_dialog_from_home(context):
    context.dialog = MessageDialogPage(context.driver, context.base_url)
    context.messages_page = MessagesPage(context.driver, context.base_url)
    context.home_page.open_message_dialog()


@when('selecciono "Nuevo mensaje"')
def step_open_dialog_from_messages(context):
    context.dialog = MessageDialogPage(context.driver, context.base_url)
    context.messages_page.open_new_message()


@when("completo un mensaje válido")
def step_fill_valid_message(context):
    context.dialog.select_course(VALID_COURSE)
    context.dialog.fill_subject(VALID_SUBJECT)
    context.dialog.fill_body(VALID_BODY)


@when("cancelo el mensaje")
def step_cancel_message(context):
    context.dialog.cancel()


@when("envío el formulario de mensaje sin completar campos")
def step_send_empty_message(context):
    context.dialog.send()


@when("completo asunto y mensaje válidos sin seleccionar curso")
def step_fill_message_without_course(context):
    context.dialog.fill_subject(VALID_SUBJECT)
    context.dialog.fill_body(VALID_BODY)


@when('completo el mensaje con curso "{course_id}", asunto "{subject}" y cuerpo "{body}"')
def step_fill_message(context, course_id, subject, body):
    context.dialog.select_course(course_id)
    context.dialog.fill_subject(subject)
    context.dialog.fill_body(body)


@when("envío el formulario de mensaje")
def step_send_message(context):
    context.dialog.send()


@when("recargo la página")
def step_refresh_page(context):
    context.driver.refresh()
    context.messages_page = MessagesPage(context.driver, context.base_url)
    context.messages_page.wait_visible(context.messages_page.VIEW)


@then("se muestra una bandeja de mensajes vacía")
def step_verify_empty_messages(context):
    if not hasattr(context, "messages_page"):
        context.messages_page = MessagesPage(context.driver, context.base_url)
    if not context.messages_page.is_visible():
        context.messages_page.open_messages()
    assert "Todavía no has enviado mensajes" in context.messages_page.empty_text()


@then("se abre el diálogo de redacción con Curso, Asunto y Mensaje")
def step_verify_dialog_fields(context):
    assert context.dialog.is_open(), "El diálogo de redacción no está abierto."
    assert context.driver.find_element(*context.dialog.COURSE).is_displayed()
    assert context.driver.find_element(*context.dialog.SUBJECT).is_displayed()
    assert context.driver.find_element(*context.dialog.BODY).is_displayed()


@then("el diálogo de redacción está cerrado")
def step_verify_dialog_closed(context):
    assert context.dialog.is_closed(), "El diálogo de redacción continúa abierto."


@then("el diálogo de redacción permanece abierto")
def step_verify_dialog_open(context):
    assert context.dialog.is_open(), "El diálogo de redacción se cerró inesperadamente."


@then('se muestra el error "{expected_error}"')
def step_verify_exact_error(context, expected_error):
    assert context.dialog.feedback() == expected_error


@then('se muestra un error que contiene "{expected_text}"')
def step_verify_partial_error(context, expected_text):
    assert expected_text in context.dialog.feedback()


@then('se muestra la confirmación "{expected_text}"')
def step_verify_toast(context, expected_text):
    assert context.messages_page.toast_text() == expected_text


@then('la bandeja contiene el mensaje "{subject}" con el texto "{body}" para "{teacher}"')
def step_verify_message_entry(context, subject, body, teacher):
    assert context.messages_page.contains_message(subject, body, teacher), (
        "No se encontró el mensaje esperado en la bandeja."
    )
