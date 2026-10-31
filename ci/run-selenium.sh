#!/usr/bin/env sh
set -u

container_name="${COMPOSE_PROJECT_NAME:-ci}-selenium-results"
docker rm -f "$container_name" >/dev/null 2>&1 || true

set +e
docker compose --profile tests run --name "$container_name" selenium-tiendademo \
  python -m pytest selenium/tests -v --junitxml=reports/resultados.xml
status=$?
set -e

mkdir -p reports/selenium
docker cp "$container_name:/tests/reports/." reports/selenium/ || true
docker rm -f "$container_name" >/dev/null 2>&1 || true

exit "$status"
