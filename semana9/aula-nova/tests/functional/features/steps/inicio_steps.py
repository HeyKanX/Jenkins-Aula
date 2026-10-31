from behave import given, then
from pages.home_page import HomePage


@given("que abro Aula Nova")
def step_open_aula_nova(context):
    context.home_page = HomePage(context.driver, context.base_url)
    context.home_page.open_home()


@then('se muestra el encabezado "{expected_text}"')
def step_verify_greeting(context, expected_text):
    actual_text = context.home_page.greeting_text()
    assert expected_text in actual_text, (
        f"Se esperaba encontrar '{expected_text}', "
        f"pero se mostró '{actual_text}'."
    )


@then("la vista Inicio está visible")
def step_verify_home_view(context):
    assert context.home_page.is_home_visible(), (
        "La vista Inicio no está visible."
    )


@then('la URL termina en "{expected_hash}"')
def step_verify_url_hash(context, expected_hash):
    assert context.driver.current_url.endswith(expected_hash), (
        f"Se esperaba una URL terminada en '{expected_hash}', "
        f"pero se obtuvo '{context.driver.current_url}'."
    )

@then("el resumen académico muestra 3 tarjetas")
def step_verify_summary_cards(context):
    actual_count = context.home_page.summary_card_count()

    assert actual_count == 3, (
        f"Se esperaban 3 tarjetas en el resumen, "
        f"pero se encontraron {actual_count}."
    )


@then('la tarjeta "{label}" muestra "{expected_value}"')
def step_verify_summary_value(context, label, expected_value):
    actual_value = context.home_page.summary_value(label)

    assert actual_value == expected_value, (
        f"Para '{label}' se esperaba '{expected_value}', "
        f"pero se obtuvo '{actual_value}'."
    )


@then("el listado resumido muestra exactamente estos cursos:")
def step_verify_dashboard_courses(context):
    expected_courses = [row["curso"] for row in context.table]
    actual_courses = context.home_page.dashboard_course_names()

    assert actual_courses == expected_courses, (
        f"Se esperaban los cursos {expected_courses}, "
        f"pero se mostraron {actual_courses}."
    )
