from behave import then, when
from pages.home_page import HomePage
from pages.profile_page import ProfilePage


@when('selecciono "Mi perfil" en el menú')
def step_open_profile_from_menu(context):
    context.home_page.wait_clickable(("css selector", "a[data-view='perfil']")).click()
    context.profile_page = ProfilePage(context.driver, context.base_url)


@when("selecciono el perfil desde el encabezado")
def step_open_profile_from_header(context):
    context.home_page.open_profile()
    context.profile_page = ProfilePage(context.driver, context.base_url)


@then("se muestra la vista Mi perfil")
def step_verify_profile_view(context):
    assert context.profile_page.is_visible(), "La vista Mi perfil no está visible."


@then('el perfil muestra nombre "{name}", código "{code}", correo "{email}" y programa "{program}"')
def step_verify_profile_details(context, name, code, email, program):
    assert context.profile_page.name() == name
    assert context.profile_page.code() == code
    assert context.profile_page.email() == email
    assert context.profile_page.program() == program


@then('el breadcrumb de perfil muestra "{expected_text}"')
def step_verify_profile_breadcrumb(context, expected_text):
    assert context.profile_page.breadcrumb() == expected_text, (
        f"Se esperaba el breadcrumb '{expected_text}'."
    )
