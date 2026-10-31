#!/usr/bin/env sh
set -eu

# Node genera el informe JUnit dentro del volumen compartido del proyecto.
docker compose exec -T aula-nova sh -lc \
  'node --test --test-reporter=junit backend/server.test.js' \
  > reports/unit/resultados.xml
