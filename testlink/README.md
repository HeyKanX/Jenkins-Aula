# Integración automática con TestLink

`register_results.py` publica los resultados que dejan Selenium, Playwright, Behave funcional y Grafana k6 en el proyecto, plan y Build de la Semana 11.

Variables requeridas:

- `TESTLINK_URL`: URL XML-RPC, por ejemplo `http://app/lib/api/xmlrpc/v1/xmlrpc.php` desde la red Docker `testlink`.
- `TESTLINK_DEVKEY`: clave API personal del usuario de TestLink. Debe guardarse como secreto, nunca en este repositorio.

Variables con valores por defecto:

- Proyecto: `Semana 11 - TiendaDemo y Aula Nova`
- Plan: `Plan de Pruebas - Semana 11`
- Build: `Build CI - Semana 11`

El reporte de cada publicación queda en `reports/testlink/resultados-testlink.json` y se archiva como evidencia del pipeline.
