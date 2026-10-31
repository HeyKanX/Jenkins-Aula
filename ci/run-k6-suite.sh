#!/usr/bin/env sh
set -u

suite="${1:?Indica la suite k6: rendimiento, estres o seguridad}"
scripts_dir="semana9/aula-nova/k6/${suite}"

if [ ! -d "$scripts_dir" ]; then
  echo "No existe la suite k6: $suite" >&2
  exit 2
fi

mkdir -p "reports/k6/${suite}"
status=0
index=0

for script in "$scripts_dir"/*.js; do
  [ -f "$script" ] || continue
  name=$(basename "$script" .js)
  container_name="${COMPOSE_PROJECT_NAME:-ci}-k6-${suite}-${index}"
  docker rm -f "$container_name" >/dev/null 2>&1 || true
  echo "Ejecutando $suite/$name"

  set +e
  docker compose --profile tests run --name "$container_name" k6 run \
    --summary-export="/reports/${name}.json" \
    "/scripts/${suite}/${name}.js"
  result=$?
  set -e

  docker cp "$container_name:/reports/." "reports/k6/${suite}/" || true
  docker rm -f "$container_name" >/dev/null 2>&1 || true
  [ "$result" -eq 0 ] || status=1
  index=$((index + 1))
done

exit "$status"
