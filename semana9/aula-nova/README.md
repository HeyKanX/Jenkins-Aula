# Aula Nova — Aula virtual universitaria

Aplicación de demostración para estudiantes universitarios con perfil académico, cursos matriculados, calificaciones por evaluación y comunicación con docentes.

## Requisitos para ejecutar la aplicación

- Node.js 18 o posterior (no requiere paquetes npm externos).

## Iniciar

Desde la raíz del proyecto:

```powershell
npm start
```

Abre <http://localhost:3000>. Para usar otro puerto, define `PORT` antes de iniciar:

```powershell
$env:PORT = "4000"
npm start
```

En macOS/Linux: `PORT=4000 npm start`.

## Pruebas automatizadas

Las pruebas del servidor usan el ejecutor nativo de Node.js:

```powershell
npm test
```

## Pruebas funcionales con Selenium y Behave (opcional)

Requisitos: Python 3.10 o posterior, Google Chrome y Node.js 18 o posterior. Selenium Manager obtiene el controlador de Chrome cuando se ejecutan las pruebas; se necesita conexión a Internet la primera vez.

Crea el entorno virtual **en el equipo de destino** (no copies `.venv` entre equipos):

```powershell
py -m venv .venv
.venv\Scripts\python.exe -m pip install -r tests/functional/requirements.txt
```

En macOS/Linux:

```bash
python3 -m venv .venv
.venv/bin/python -m pip install -r tests/functional/requirements.txt
```

Inicia la aplicación en una terminal:

```powershell
npm start
```

En otra terminal, ejecuta los escenarios:

```powershell
.venv\Scripts\python.exe -m behave tests/functional/features
```

Las capturas generadas se guardan en `tests/functional/evidencias/`.

## Pruebas de carga y seguridad con k6 (opcional)

Instala k6 en el sistema siguiendo la documentación oficial de Grafana. Inicia la aplicación y ejecuta cualquier escenario desde la raíz, por ejemplo:

```powershell
k6 run k6/rendimiento/rendimiento_01_carga_inicio.js
```

Los escenarios usan `http://127.0.0.1:3000` por defecto. Para apuntarlos a otro host o puerto, define `BASE_URL`:

```powershell
$env:BASE_URL = "http://localhost:4000"
k6 run k6/rendimiento/rendimiento_01_carga_inicio.js
```

En macOS/Linux: `BASE_URL=http://localhost:4000 k6 run k6/rendimiento/rendimiento_01_carga_inicio.js`.

## Estructura

- `app/`: interfaz web adaptable (HTML, CSS y JavaScript).
- `backend/`: servidor HTTP, API y pruebas automatizadas.
- `tests/functional/`: escenarios Behave, páginas Selenium y capturas.
- `k6/`: escenarios de rendimiento, estrés y seguridad.

La API ofrece `GET /api/student`, `GET /api/courses`, `GET /api/messages` y `POST /api/messages`. El perfil, los cursos y las calificaciones son datos de demostración; los mensajes se mantienen en memoria mientras el servidor está activo.
