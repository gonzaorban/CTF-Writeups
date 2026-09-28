# get_reactapp.py — download the FULL main.js served at /images/<nil-uuid>/main.js and extract
# the APP CODE (after the React bundle): fetch/axios calls, API endpoints, SQL-ish strings,
# route names, and any UUIDs. Also grab the HTML host page under /images/<uuid>/.
import requests, re
BASE = "https://chl-f4e46c02-efed-4276-8edf-ffade8aa3cf6-mis-viajes-v2.softwareseguro.com.ar"
NIL  = "00000000-0000-0000-0000-000000000000"
UID  = "ea42cd39-001b-4fb5-a509-449322674687"

# 1) the HTML page that mounts this React app
for host in [f"/images/{NIL}", f"/images/{NIL}/", f"/images/{UID}", f"/images/{UID}/"]:
    r = requests.get(BASE+host)
    print(f"{host:48} -> {r.status_code} len={len(r.text)} ct={r.headers.get('Content-Type','')}")
    if r.status_code==200 and "text/html" in r.headers.get("Content-Type",""):
        open("react_index.html","w",encoding="utf-8").write(r.text)
        print("   saved react_index.html")

# 2) the full bundle
r = requests.get(f"{BASE}/images/{NIL}/main.js")
js = r.text
open("main_full.js","w",encoding="utf-8").write(js)
print(f"\nmain.js full size: {len(js)} bytes")

# 3) extract endpoints / fetch / api / interesting strings from the WHOLE bundle
print("\n--- fetch/axios/api endpoints ---")
pats = [r'fetch\(\s*[`"\']([^`"\']+)', r'axios\.\w+\(\s*[`"\']([^`"\']+)',
        r'[`"\'](/api/[^`"\']+)', r'[`"\'](/images/[^`"\']*)', r'[`"\'](/uploads/[^`"\']*)',
        r'[`"\'](/admin[^`"\']*)', r'[`"\'](/[a-z_]+/\$\{[^}]+\})']
seen=set()
for p in pats:
    for m in re.findall(p, js):
        if m not in seen and len(m)<200:
            seen.add(m); print("  ", m)

print("\n--- template-literal URLs with vars (likely API calls) ---")
for m in set(re.findall(r'`(/[^`]*\$\{[^`]*)`', js)):
    print("  ", m[:120])

print("\n--- SQL-ish / interesting words ---")
for kw in ["SELECT","INSERT","query","flag","code","codigo","gana","winner","admin","user_id","search","filter"]:
    hits = [m.start() for m in re.finditer(re.escape(kw), js)]
    if hits:
        # print a small context around the first hit
        i = hits[0]; ctx = js[max(0,i-40):i+60].replace("\n"," ")
        print(f"  {kw} ({len(hits)}x): ...{ctx}...")

print("\n--- UUIDs in bundle (other than ours) ---")
for m in set(re.findall(r"[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}", js)):
    if m not in (UID, NIL):
        print("  ", m)
