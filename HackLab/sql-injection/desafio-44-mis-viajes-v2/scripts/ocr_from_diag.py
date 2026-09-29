# ocr_from_diag.py — DIAGNÓSTICO OCR de la secuencia `FROM images`.
#
# Objetivo de esta fase (medir, no exploitar): la SQLi vía OCR está confirmada, pero toda
# subconsulta con `FROM images` da 500 porque el OCR deforma/reordena esa secuencia y el SQL
# resultante es inválido. Para VERLO, pintamos las variantes como LITERAL PLANO (sin el
# envoltorio ejecutable `9'||(...)||'9`), así el INSERT nunca rompe y summary_ocr guarda
# EXACTAMENTE lo que el OCR leyó. Comparamos entrada vs salida carácter por carácter.
#
# No exploita: solo lee cómo el OCR reproduce cada forma de escribir "FROM images".
# Uso: correr desde la carpeta del desafío (usa assets/paisaje.png). Actualizar BASE por spawn.
import requests, base64, re, sys, os
from PIL import Image, ImageDraw, ImageFont
import piexif

BASE = "https://chl-5164f230-2a03-41d3-b9a5-9d2931b34c94-mis-viajes-v2.softwareseguro.com.ar"
PAISAJE = "assets/paisaje.png" if os.path.exists("assets/paisaje.png") else "paisaje.png"

html = requests.get(BASE + "/").text
UID = re.search(r'([0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12})', html).group(1)
base_img = Image.open(PAISAJE).convert("RGB")


def font(sz):
    for p in ["C:/Windows/Fonts/consolab.ttf", "C:/Windows/Fonts/cour.ttf"]:
        try:
            return ImageFont.truetype(p, sz)
        except Exception:
            pass
    return ImageFont.load_default()


def build(text, fname, size=30):  # formato EXACTO que el OCR lee bien (de v2_exact.py)
    W = min(2000, max(1000, 40 + int(len(text) * size * 0.56)))
    H = 260
    img = base_img.resize((W, H))
    d = ImageDraw.Draw(img)
    f = font(size)
    bb = d.textbbox((20, 20), text, font=f)
    d.rectangle([0, 0, W, bb[3] + 20], fill=(255, 255, 255))
    d.text((20, 20), text, font=f, fill=(0, 0, 0))
    img.save(fname, "jpeg", quality=72, optimize=True)

    def dms(x):
        dd = int(x); mm = int((x - dd) * 60); s = round((x - dd - mm / 60) * 3600, 4)
        return ((dd, 1), (mm, 1), (int(s * 100), 100))
    ex = {'0th': {piexif.ImageIFD.Make: b'Samsung', piexif.ImageIFD.Model: b'Galaxy S25'},
          'Exif': {piexif.ExifIFD.DateTimeOriginal: b'2025:10:01 23:51:37'},
          'GPS': {piexif.GPSIFD.GPSLatitudeRef: b'S', piexif.GPSIFD.GPSLatitude: dms(41.13),
                  piexif.GPSIFD.GPSLongitudeRef: b'W', piexif.GPSIFD.GPSLongitude: dms(71.31)}}
    piexif.insert(piexif.dump(ex), fname)
    return "data:image/jpeg;base64," + base64.b64encode(open(fname, "rb").read()).decode()


def diag(painted, desc):
    fname = f"diag_{desc}.jpg"
    uri = build(painted, fname)
    r = requests.post(f"{BASE}/upload", json={"image": uri, "description": desc, "user_id": UID})
    ocr = ""
    if r.status_code == 200:
        data = requests.get(f"{BASE}/images/{UID}").json()
        row = next((x for x in data if x.get("description") == desc), None)
        ocr = row.get("summary_ocr", "") if row else ""
    match = "==" if ocr == painted else "!="
    print(f"[{desc}] {r.status_code}")
    print(f"    IN : {painted!r}")
    print(f"    OUT: {ocr!r}   {match}")
    return ocr


# Variantes de "SELECT user_id FROM images WHERE id=1" como literal plano.
# Queremos ver: ¿mueve FROM? ¿pega/parte palabras? ¿cambia mayúsculas? ¿pierde el espacio?
print(f"UID propio: {UID}\n=== cómo lee el OCR la frase con FROM images (literal plano) ===\n")
diag("SELECT user_id FROM images WHERE id=1", "plain_full")
diag("FROM images", "from_only")
diag("images FROM images", "from_repeat")
diag("SELECT x FROM images", "short_from")
diag("aaa FROM images bbb", "from_padded")
diag("FROM  images", "from_2space")
diag("FROM_images", "from_underscore")
diag("FROM\timages", "from_tab")
