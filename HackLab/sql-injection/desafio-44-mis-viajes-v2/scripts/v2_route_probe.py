# v2_route_probe.py — All those paths report Allow: GET but GET->404. This is Flask returning
# the app-wide allowed methods for a path that MATCHES a rule but fails inside (e.g. the <uuid>
# converter or a 404 raised in the view). Clarify: is /search its own route, or is everything
# funneling through /images/<uuid>? Compare 404 bodies and test GET variants.
import requests, re

BASE = "https://chl-453bbf5a-0b09-4ad8-a4f2-61aeaba1384e-mis-viajes-v2.softwareseguro.com.ar"
html = requests.get(BASE+"/").text
UID = re.search(r'([0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12})', html).group(1)

def show(path):
    r = requests.get(BASE+path)
    ln = len(r.text)
    # the standard flask 404 page has a known length; note it
    print(f"GET {path:48} -> {r.status_code} len={ln}")
    return r.status_code, ln

print("-- compare 404 bodies to tell real routes from generic 404 --")
show("/definitely_not_a_route_xyz")     # baseline generic 404
show("/search")
show("/images/search")
show("/api/search")
show(f"/images/{UID}")                   # the known-good one
show("/images/not-a-uuid")               # uuid converter fail
print()

# If /search is a REAL route that needs a param, try common param names via GET
print("-- try GET /search with params --")
for qp in ["", "?q=a", "?query=a", "?term=a", "?text=a", "?ocr=a", "?user_id="+UID, "?id=1", "?name=a"]:
    r = requests.get(f"{BASE}/search{qp}")
    print(f"/search{qp:24} -> {r.status_code} len={len(r.text)}")
