# trace_mainjs.py — Python got 404 for /images/<uuid>/main.js but the browser shows a React
# bundle there. Maybe it needs specific headers (Accept, Referer) or a different casing, or the
# path is a client-side route. Try variations and see what actually returns JS.
import requests
BASE = "https://chl-f4e46c02-efed-4276-8edf-ffade8aa3cf6-mis-viajes-v2.softwareseguro.com.ar"
NIL  = "00000000-0000-0000-0000-000000000000"

variations = [
    f"/images/{NIL}/main.js",
    "/main.js",
    "/static/main.js",
    "/build/main.js",
    "/static/js/main.js",
    "/assets/index.js",
    "/bundle.js",
]
headers_sets = [
    {},
    {"Accept": "application/javascript,*/*"},
    {"Referer": f"{BASE}/images/{NIL}"},
]
for path in variations:
    for h in headers_sets:
        r = requests.get(BASE+path, headers=h, timeout=10)
        ct = r.headers.get("Content-Type","")
        if r.status_code==200 and ("javascript" in ct or len(r.content)>1000):
            print(f"HIT {path}  headers={h}  -> {r.status_code} {ct} len={len(r.content)}")
            open("bundle_found.js","wb").write(r.content)
            print("  saved bundle_found.js")
            break
    else:
        continue
    break
else:
    print("no direct JS path worked from Python.")
    print("The React bundle is likely served by the HackLab platform wrapper, not the challenge app.")
    print("Confirm in browser: right-click main.js in Sources -> 'Copy link address' and share it.")
