#!/usr/bin/env sh
set -u

container_name="${COMPOSE_PROJECT_NAME:-ci}-playwright-results"
docker rm -f "$container_name" >/dev/null 2>&1 || true

set +e
docker compose --profile tests run --name "$container_name" playwright-tiendademo \
  python -m pytest playwright_tests/tests -v --junitxml=reports/resultados.xml
status=$?
set -e

mkdir -p reports/playwright
docker cp "$container_name:/tests/reports/." reports/playwright/ || true
docker rm -f "$container_name" >/dev/null 2>&1 || true

exit "$status"
