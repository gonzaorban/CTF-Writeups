# get_mainjs.py — fetch main.js from likely paths and scan it for UUIDs, endpoints, SQL hints.
import requests, re
BASE = "https://chl-f4e46c02-efed-4276-8edf-ffade8aa3cf6-mis-viajes-v2.softwareseguro.com.ar"
UID  = "ea42cd39-001b-4fb5-a509-449322674687"

candidates = [
    "/main.js",
    f"/images/{UID}/main.js",
    "/images/main.js",
    "/static/main.js",
    "/js/main.js",
    "/assets/main.js",
    f"/uploads/main.js",
]
for p in candidates:
    try:
        r = requests.get(BASE+p, timeout=10)
        ct = r.headers.get("Content-Type","")
        print(f"{p:40} -> {r.status_code} {ct} len={len(r.content)}")
        if r.status_code==200 and ("javascript" in ct or "text" in ct) and len(r.content)>0:
            open("main_dump.js","wb").write(r.content)
            print("   >>> saved main_dump.js")
    except Exception as e:
        print(f"{p} ERR {e}")
