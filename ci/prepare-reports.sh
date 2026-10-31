#!/usr/bin/env sh
set -eu

rm -rf reports
mkdir -p reports/unit reports/selenium reports/playwright
mkdir -p reports/k6/rendimiento reports/k6/estres reports/k6/seguridad

rm -rf semana9/aula-nova/tests/functional/reports
mkdir -p semana9/aula-nova/tests/functional/reports
