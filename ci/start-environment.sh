#!/usr/bin/env sh
set -eu

# Solo inicia los servicios persistentes. Las suites se ejecutan aparte con
# "docker compose run", para que cada una tenga su propio resultado.
docker compose --profile tests up -d --wait aula-nova tienda-demo selenium
