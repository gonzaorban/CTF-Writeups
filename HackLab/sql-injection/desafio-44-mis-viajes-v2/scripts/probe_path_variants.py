# probe_path_variants.py — the GET uses Flask <uuid> converter (rejects non-uuid w/ 404).
# But maybe an ALTERNATE path or method accepts a free string we can inject, OR the uuid
# converter can be bypassed. Test methods + trailing content + alternate content-types.
import requests
BASE = "https://chl-f4e46c02-efed-4276-8edf-ffade8aa3cf6-mis-viajes-v2.softwareseguro.com.ar"
UID  = "ea42cd39-001b-4fb5-a509-449322674687"

tests = [
    ("GET  normal",        "GET",  f"/images/{UID}"),
    ("POST to images",     "POST", f"/images/{UID}"),
    ("GET uppercase seg",  "GET",  f"/images/{UID.upper()}"),
    ("GET with .json",     "GET",  f"/images/{UID}.json"),
    ("GET double slash",   "GET",  f"/images//{UID}"),
    ("GET trailing slash", "GET",  f"/images/{UID}/"),
    ("GET semicolon",      "GET",  f"/images/{UID};"),
    # uuid-shaped but with an injected OR via all-hex? not possible. Try a valid uuid that is
    # the NIL and see if any query returns victim rows via a UNION in a different param:
]
for name, method, path in tests:
    try:
        r = requests.request(method, BASE+path, timeout=10)
        n = -1
        try: n=len(r.json())
        except: pass
        print(f"{name:20} {method:4} {path[-45:]:46} -> {r.status_code} rows={n}")
    except Exception as e:
        print(f"{name} ERR {e}")
