# build a valid geo-JPEG and the exact JSON payload the app expects
# pip install piexif pillow requests
from PIL import Image
import piexif, base64, json, requests

# 1) valid JPEG
Image.new("RGB", (800, 600), (90, 140, 180)).save("trip.jpg", "jpeg")

def dms(dec):
    d=int(dec); m=int((dec-d)*60); s=round((dec-d-m/60)*3600,4)
    return ((d,1),(m,1),(int(s*100),100))

lat, lon = -41.13, -71.31
exif = {
  "0th": {piexif.ImageIFD.Make:b"Samsung", piexif.ImageIFD.Model:b"Galaxy S25"},
  "Exif": {piexif.ExifIFD.DateTimeOriginal:b"2025:10:01 23:51:37"},
  "GPS": {
    piexif.GPSIFD.GPSLatitudeRef:b"S", piexif.GPSIFD.GPSLatitude:dms(abs(lat)),
    piexif.GPSIFD.GPSLongitudeRef:b"W", piexif.GPSIFD.GPSLongitude:dms(abs(lon)),
  },
}
piexif.insert(piexif.dump(exif), "trip.jpg")

# 2) data URI
b64 = base64.b64encode(open("trip.jpg","rb").read()).decode()
data_uri = "data:image/jpeg;base64," + b64

# 3) send it exactly like the frontend does
BASE = "https://chl-f4e46c02-efed-4276-8edf-ffade8aa3cf6-mis-viajes-v2.softwareseguro.com.ar"
payload = {
    "description": "probando",
    "image": data_uri,
    "user_id": "ea42cd39-001b-4fb5-a509-449322674687",  # tu user_id
}
r = requests.post(f"{BASE}/upload", json=payload)  # add cookies=... if there's a session
print(r.status_code, r.text)
