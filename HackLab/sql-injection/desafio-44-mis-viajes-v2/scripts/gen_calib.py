# gen_calib.py — calibrate painted-quotes -> delivered-quotes -> status.
# Paint N doubled quotes inside SELECT context; readback shows how many the OCR delivered,
# and status (500=odd/broke, 200=balanced) tells us the exact count that reaches SQL.
from PIL import Image, ImageDraw, ImageFont
import piexif, base64

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
# paint n quotes (glued) between SELECT-context words; record file per n
for n in range(1,9):
    text = "SELECT " + (q*n) + " FROM images"
    open(f"cal{n}_datauri.txt","w").write(build(text, f"cal{n}.jpg"))
print("built cal1..cal8 (n painted quotes each, SELECT context)")
