# Proyecto de Calidad - Semanas 8, 9 y 11

Repositorio unificado para las actividades de automatizacion de pruebas e integracion continua.

## Estructura

- `semana8/tienda-demo/`: TiendaDemo y sus 41 casos Selenium, 41 casos Playwright y 41 escenarios de aceptacion Behave.
- `semana9/aula-nova/`: Aula Nova, 20 casos funcionales Selenium/Behave y escenarios k6 de rendimiento, estres y seguridad.
- `Jenkinsfile`: pipeline actual de Aula Nova, adaptado a la nueva estructura.
- `Dockerfile.jenkins`: imagen de Jenkins con Node.js, Python, Chromium y k6.

La proxima etapa incorporara ambos proyectos en los pipelines y agregara Docker Compose, GitHub Actions y TestLink de acuerdo con la actividad de la Semana 11.
