from behave import then, when
from pages.courses_page import CoursesPage
from pages.home_page import HomePage


@when('selecciono "Mis cursos" en el menú')
def step_open_courses(context):
    context.home_page.open_courses()
    context.courses_page = CoursesPage(context.driver, context.base_url)


@then("se muestra la vista Mis cursos")
def step_verify_courses_view(context):
    assert context.courses_page.is_visible(), "La vista Mis cursos no está visible."


@then('el breadcrumb muestra "{expected_text}"')
def step_verify_courses_breadcrumb(context, expected_text):
    assert context.courses_page.breadcrumb() == expected_text, (
        f"Se esperaba el breadcrumb '{expected_text}'."
    )


@then("se muestran {expected_count:d} tarjetas de curso")
def step_verify_course_card_count(context, expected_count):
    assert context.courses_page.course_count() == expected_count, (
        f"Se esperaban {expected_count} tarjetas de curso."
    )


@then('el curso "{course_name}" muestra código "{code}", docente "{teacher}", aula "{room}" y créditos "{credits}"')
def step_verify_course_details(context, course_name, code, teacher, room, credits):
    details = context.courses_page.course_details(course_name)
    assert details == {
        "codigo": code,
        "docente": teacher,
        "aula": room,
        "creditos": credits,
    }, f"Los datos del curso no coinciden: {details}."
