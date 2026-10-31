from pathlib import Path
import pytest


BASE_DIR = Path(__file__).resolve().parents[1]

TEMP_DIR = BASE_DIR / "evidencias" / "playwright" / "temporales"
FALLOS_DIR = BASE_DIR / "evidencias" / "playwright" / "fallos"


def pytest_collection_modifyitems(items):
    """
    Envuelve automáticamente el tearDown de todas las clases unittest
    para tomar una captura antes de cerrar el navegador.
    """

    clases_modificadas = set()

    for item in items:
        clase = getattr(item, "cls", None)

        if clase is None or clase in clases_modificadas:
            continue

        tear_down_original = getattr(clase, "tearDown", None)

        if tear_down_original is None:
            continue

        def crear_teardown(original):

            def nuevo_teardown(self):

                page = getattr(self, "page", None)

                if page is not None:
                    TEMP_DIR.mkdir(parents=True, exist_ok=True)

                    nombre_test = getattr(
                        self,
                        "_testMethodName",
                        "test_desconocido"
                    )

                    ruta = TEMP_DIR / f"{nombre_test}.png"

                    try:
                        page.screenshot(
                            path=str(ruta),
                            full_page=True
                        )
                    except Exception as error:
                        print(
                            f"No se pudo tomar captura de "
                            f"{nombre_test}: {error}"
                        )

                original(self)

            return nuevo_teardown

        clase.tearDown = crear_teardown(tear_down_original)

        clases_modificadas.add(clase)


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):

    outcome = yield
    report = outcome.get_result()

    if report.when != "call":
        return

    nombre_test = item.name

    origen = TEMP_DIR / f"{nombre_test}.png"

    if not origen.exists():
        return

    if report.failed:

        FALLOS_DIR.mkdir(parents=True, exist_ok=True)

        destino = FALLOS_DIR / f"{nombre_test}.png"

        origen.replace(destino)

        print(f"\nEvidencia de fallo guardada: {destino}")

    else:
        # Si el test pasó, eliminamos la captura temporal.
        origen.unlink()