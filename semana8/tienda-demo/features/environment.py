"""Libera el navegador al finalizar cada escenario Behave."""
def after_scenario(context, scenario):
    driver = getattr(context, "driver", None)
    if driver:
        driver.quit()
        context.driver = None

