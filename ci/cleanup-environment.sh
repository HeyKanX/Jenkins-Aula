#!/usr/bin/env sh
set -eu

docker compose --profile tests down --volumes --remove-orphans
