#!/usr/bin/env python3
"""Replica el POST multipart que hace la app (Api.verificar) contra el endpoint
real, con los datos y las fotos del objetivo. Imprime la respuesta del servidor
(incluido el token/URL del certificado si la verificacion pasa).

Uso: python verificar.py forjado-frente.png forjado-dorso.png
"""
import sys
import json
import uuid
import urllib.request
import urllib.error

URL = "https://auth.shared.softwareseguro.com.ar/api/verificar"

# Datos del objetivo (KAIRA LOM VENKRA DOSS).
CAMPOS = {
    "apellido": "VENKRA DOSS",
    "nombre": "KAIRA LOM",
    "matricula": "MRC-48217390",
    "sexo": "F",
    "fecha_nacimiento": "14/03/0219",
}


def multipart(campos, frente, dorso):
    boundary = "----vk" + uuid.uuid4().hex
    b = boundary.encode()
    body = b""
    for k, v in campos.items():
        body += b"--" + b + b"\r\n"
        body += ('Content-Disposition: form-data; name="%s"\r\n\r\n' % k).encode()
        body += v.encode() + b"\r\n"
    for field, path, fn in (("foto_frente", frente, "frente.jpg"),
                            ("foto_dorso", dorso, "dorso.jpg")):
        with open(path, "rb") as f:
            data = f.read()
        body += b"--" + b + b"\r\n"
        body += ('Content-Disposition: form-data; name="%s"; filename="%s"\r\n'
                 % (field, fn)).encode()
        body += b"Content-Type: image/jpeg\r\n\r\n" + data + b"\r\n"
    body += b"--" + b + b"--\r\n"
    return boundary, body


def main():
    frente, dorso = sys.argv[1], sys.argv[2]
    boundary, body = multipart(CAMPOS, frente, dorso)
    req = urllib.request.Request(URL, data=body, method="POST")
    req.add_header("Content-Type", "multipart/form-data; boundary=%s" % boundary)
    req.add_header("User-Agent", "okhttp/4.12.0")
    try:
        r = urllib.request.urlopen(req, timeout=40)
        print(json.dumps(json.loads(r.read()), indent=2, ensure_ascii=False))
    except urllib.error.HTTPError as e:
        print("HTTP", e.code)
        print(e.read().decode("utf-8", "replace"))


if __name__ == "__main__":
    main()
