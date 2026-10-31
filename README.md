# Proyecto de Calidad - Semanas 8, 9 y 11

Repositorio unificado para las actividades de automatizacion de pruebas e integracion continua.

## Estructura

- `semana8/tienda-demo/`: TiendaDemo y sus 41 casos Selenium, 41 casos Playwright y 41 escenarios de aceptacion Behave.
- `semana9/aula-nova/`: Aula Nova, 20 casos funcionales Selenium/Behave y escenarios k6 de rendimiento, estres y seguridad.
- `ci/`: comandos compartidos para preparar reportes, levantar Docker, ejecutar las suites y limpiar el entorno.
- `.github/workflows/ci.yml`: workflow de GitHub Actions con las mismas etapas del pipeline Jenkins.
- `Jenkinsfile`: pipeline Docker para las dos aplicaciones y sus suites automatizadas.
- `Dockerfile.jenkins`: imagen de Jenkins con el cliente Docker, Node.js, Python y k6.

La integración automática de resultados con TestLink se agregará después de configurar el proyecto, el plan de pruebas y las credenciales en esa herramienta.
