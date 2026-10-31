#!/usr/bin/env sh
set -u

container_name="${COMPOSE_PROJECT_NAME:-ci}-functional-results"
docker rm -f "$container_name" >/dev/null 2>&1 || true

set +e
docker compose --profile tests run --name "$container_name" funcional-aula-nova
status=$?
set -e

mkdir -p semana9/aula-nova/tests/functional/reports
mkdir -p semana9/aula-nova/tests/functional/evidencias
docker cp "$container_name:/app/tests/functional/reports/." semana9/aula-nova/tests/functional/reports/ || true
docker cp "$container_name:/app/tests/functional/evidencias/." semana9/aula-nova/tests/functional/evidencias/ || true
docker rm -f "$container_name" >/dev/null 2>&1 || true

exit "$status"
