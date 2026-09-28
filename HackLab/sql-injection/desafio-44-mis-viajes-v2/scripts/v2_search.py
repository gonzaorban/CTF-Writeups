# v2_search.py — summary_ocr stored as bound param (safe on INSERT). Hint: "OCR + some SQL".
# Maybe there is a SEARCH endpoint that queries by OCR text, OR the stored OCR is used in a
# second query. Probe for search/filter endpoints and query params that take user text into SQL.
import requests, re

BASE = "https://chl-453bbf5a-0b09-4ad8-a4f2-61aeaba1384e-mis-viajes-v2.softwareseguro.com.ar"
html = requests.get(BASE+"/").text
UID = re.search(r'([0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12})', html).group(1)

# candidate search/filter endpoints and params
endpoints = [
    "/search", "/api/search", "/images/search", "/buscar", "/filter",
    f"/search?q=test", f"/images?q=test", f"/images?search=test",
    f"/images/{UID}?q=test", f"/images/{UID}?search=paisaje",
    f"/images/{UID}?classification=paisaje", f"/images/{UID}?ocr=test",
    f"/images/{UID}?order=id", f"/images/{UID}?sort=id",
]
print("-- endpoint/param discovery --")
base_rows = len(requests.get(f"{BASE}/images/{UID}").json())
print("baseline /images rows:", base_rows)
for e in endpoints:
    try:
        r = requests.get(BASE+e, timeout=10)
        n=-1
        try: n=len(r.json())
        except: pass
        diff = "" if n==base_rows or n==-1 else f"  <<< rows={n} (differs!)"
        print(f"{e:42} -> {r.status_code} rows={n}{diff}")
    except Exception as ex:
        print(e, "ERR", ex)

# also POST search
print("\n-- POST search attempts --")
for path in ["/search","/images/search","/api/search"]:
    for body in [{"q":"test"},{"query":"test"},{"search":"test"},{"ocr":"test"}]:
        try:
            r=requests.post(BASE+path, json=body, timeout=10)
            if r.status_code!=404:
                print(f"POST {path} {body} -> {r.status_code} {r.text[:60].strip()}")
        except: pass
