# Proyecto TiendaDemo — Semana 8

Proyecto de pruebas funcionales y de aceptación de la aplicación TiendaDemo. La carpeta `app/` conserva la aplicación bajo prueba del ejemplo. Esta entrega reorganiza la automatización con Page Object Model (POM), Selenium y Playwright con `unittest`, y escenarios Behave.

## Estructura

- `app/` — aplicación bajo prueba en HTML, CSS y JavaScript.
- `selenium/pages/` — clases Page Object Model para Selenium.
- `selenium/tests/` — 41 pruebas Selenium organizadas en cinco módulos por rangos TC.
- `playwright/pages/` — clases Page Object Model para Playwright.
- `playwright/tests/` — 41 pruebas Playwright organizadas en los mismos cinco rangos TC.
- `features/` — cuatro archivos Gherkin con 41 escenarios de aceptación TC-01–TC-41.
- `features/steps/` — pasos Behave; cada archivo de escenarios tiene un archivo de pasos con el mismo nombre base. Los pasos utilizan Selenium.
- `utils/driver_factory.py` — configuración compartida de Chrome para Selenium y Behave.
- `evidencias/selenium/` y `evidencias/playwright/` — destinos para capturas y evidencias futuras; actualmente solo contienen `.gitkeep`.
- `requirements.txt` — dependencias del proyecto.
- `pytest.ini` — configuración del modo de importación para pytest; los comandos de ejecución documentados utilizan unittest y Behave.


## Configuración

1. Instala dependencias:

```bash
python -m pip install -r requirements.txt
python -m playwright install chromium
```

2. Ejecuta tests individuales con unittest:

```bash
python -m unittest tests/test_agregar_producto.py
python -m unittest tests/test_aplicar_cupon.py
python -m unittest tests/test_eliminar_producto.py
python -m unittest tests/test_modificar_cantidad.py
python -m unittest tests/test_validacion_checkout.py
```

## Ejecutar pruebas

### 1. Ejecutar un módulo con unittest

Ejemplo para los casos TC-01–TC-05:

```bash
python -m unittest discover -s selenium/tests -p "test_tc01_tc05.py" -v
python -m unittest discover -s playwright/tests -p "test_tc01_tc05.py" -v
```

Para ejecutar otro módulo, sustituye el patrón por uno de estos archivos:

| Archivo | Casos | Cobertura implementada |
|---|---|---|
| `test_tc01_tc05.py` | TC-01–TC-05 | Agregar productos, consultar el carrito y actualizar el contador. |
| `test_tc06_tc13.py` | TC-06–TC-13 | Modificar cantidades, eliminar productos y actualizar el subtotal. |
| `test_tc14_tc19.py` | TC-14–TC-19 | Aplicar y validar cupones, comprobar descuentos y total. |
| `test_tc20_tc31.py` | TC-20–TC-31 | Checkout, campos obligatorios, compra y confirmación. |
| `test_tc32_tc41.py` | TC-32–TC-41 | Flujos de aceptación, casos negativos y compra con descuento. |

### 2. Ejecutar todas las pruebas con unittest

Ejecuta cada suite por separado:

```bash
python -m unittest discover -s tests
python -m unittest discover -s . -p "test*.py"
```

Cada módulo contiene una clase derivada de `unittest.TestCase`. Selenium crea el navegador en `setUpClass`, abre nuevamente la aplicación y crea los Page Objects en `setUp`, y cierra el navegador en `tearDownClass`. Playwright crea el navegador por clase, utiliza un contexto y una página nuevos por prueba, y los libera al terminar.

### 3. Ejecutar Behave

```bash
behave features
```

## Qué implementa el proyecto

- Aplicación de demostración con catálogo, búsqueda, filtro por categoría, carrito, controles de cantidad y stock, cupones, checkout y confirmación de pedido.
- Automatización con POM para Selenium y Playwright, con cinco módulos por herramienta y los casos TC-01–TC-41 definidos en ambas suites.
- Escenarios de aceptación en Gherkin y automatización con Behave/Selenium.
- Pruebas positivas y negativas: productos repetidos, eliminación, carrito vacío, cupones inválidos o vacíos y validación de datos del checkout, entre otras.
- Reinicio de la aplicación entre pruebas y cierre de los navegadores al finalizar.


## Estado de las pruebas y fallos identificados

En la revisión de esta carpeta se verificó la sintaxis de todos los archivos Python y se ejecutó Behave en modo `--dry-run`: se reconocieron cuatro archivos de escenarios, 41 escenarios y 199 pasos, sin errores de correspondencia. Los escenarios quedaron sin ejecutar, como corresponde a ese modo.


TC-09 — Cantidad negativa: Este caso se encuentra omitido (skip), ya que no es posible ejecutarlo mediante la interfaz actual. El carrito únicamente dispone de botones + y − para modificar la cantidad de productos, mientras que el valor de la cantidad es de solo lectura. Por eso, no existe un campo que permita ingresar directamente un valor negativo como -1. Este caso no debe registrarse como aprobado ni como fallo funcional, sino como una prueba no ejecutable debido a las características actuales de la interfaz.

El TC-23 — Apellido obligatorio también se encuentra omitido cuando no existe un campo independiente para ingresar el apellido. El formulario de checkout solicita el nombre completo mediante un único campo, por lo que no es posible comprobar de manera independiente la validación del apellido obligatorio. Al igual que el caso anterior, debe documentarse como una prueba omitida y no como aprobada o fallida.

En el TC-17 — Cupón repetido se ha identificado un posible fallo funcional mediante la inspección del comportamiento esperado. La aplicación mantiene correctamente el descuento sin acumularlo, pero vuelve a mostrar un mensaje indicando que el cupón fue aplicado. Por esta razón, se considera un fallo esperado que deberá confirmarse mediante la ejecución de la prueba automatizada.

También se identificó, por lectura de `app/carrito.js`, que aplicar un cupón inválido después de uno válido elimina el descuento del estado sin actualizar el resumen visible del carrito. Esto puede producir una diferencia entre el importe mostrado en el carrito y el checkout. TC-15 prueba un cupón inválido sin un cupón válido previo, por lo que no cubre esa secuencia.

## Alcance de esta entrega

La entrega está organizada para el trabajo de Semana 8, según el alcance descrito en el README original. El PDF mencionado no está incluido en esta carpeta, por lo que esta revisión no permite certificar el cumplimiento de todos sus requisitos.

La matriz de trazabilidad, las capturas/evidencias, el informe de resultados, se generan exitosamente. 
