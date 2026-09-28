# probe_idparam.py — maybe the winning image is reachable by an id query-param
# or an alternate route the JS never uses.
import requests
BASE = "https://chl-f4e46c02-efed-4276-8edf-ffade8aa3cf6-mis-viajes-v2.softwareseguro.com.ar"
MY_UID = "ea42cd39-001b-4fb5-a509-449322674687"

tries = [
    f"/images/{MY_UID}?id=1",
    f"/images/{MY_UID}?user_id=1",
    "/images?id=1",
    "/images/1/",
    "/image/1",
    f"/images/{MY_UID}/1",
    "/uploads/1",
    "/upload/1",
    f"/images?user_id={MY_UID}",
]
for t in tries:
    try:
        r = requests.get(BASE + t)
        b = r.text.strip()
        print(f"{t:45} -> {r.status_code} len={len(b)} {b[:70]!r}")
    except Exception as e:
        print(t, "ERR", e)
