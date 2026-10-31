from behave import then, when
from pages.grades_page import GradesPage
from pages.home_page import HomePage


@when('selecciono "Calificaciones" en el menú')
def step_open_grades(context):
    context.home_page.open_grades()
    context.grades_page = GradesPage(context.driver, context.base_url)


@when('selecciono "Ver mi progreso"')
def step_open_grades_from_progress(context):
    context.home_page.wait_clickable(("css selector", "#view-inicio .hero-link")).click()
    context.grades_page = GradesPage(context.driver, context.base_url)


@then("se muestra la vista Calificaciones")
def step_verify_grades_view(context):
    assert context.grades_page.is_visible(), "La vista Calificaciones no está visible."


@then("la tabla de calificaciones muestra {expected_count:d} cursos")
def step_verify_grade_row_count(context, expected_count):
    assert context.grades_page.row_count() == expected_count, (
        f"Se esperaban {expected_count} cursos en la tabla."
    )


@then('la tabla contiene las columnas "{t1}", "{t2}", "{t3}" y "{final}"')
def step_verify_grade_headers(context, t1, t2, t3, final):
    headers = [header.casefold() for header in context.grades_page.headers()]
    for header in (t1, t2, t3, final):
        assert header.casefold() in headers, f"No se encontró la columna '{header}'."


@then('el curso "{course_name}" tiene T1 "{t1}", T2 "{t2}", T3 "{t3}" y Final "{final}"')
def step_verify_complete_grades(context, course_name, t1, t2, t3, final):
    assert context.grades_page.grades_for(course_name) == {
        "t1": t1,
        "t2": t2,
        "t3": t3,
        "final": final,
    }


@then('el curso "{course_name}" tiene T3 "{t3}" y Final "{final}"')
def step_verify_partial_grades(context, course_name, t3, final):
    grades = context.grades_page.grades_for(course_name)
    assert grades["t3"] == t3 and grades["final"] == final, (
        f"Se obtuvieron las notas {grades}."
    )
