# probe_userid_assign.py — how does the server assign user_id when we omit/blank it?
# If seeded rows used a default, we can discover & read it. Also: does upload RETURN the row?
import requests, json
BASE = "https://chl-f4e46c02-efed-4276-8edf-ffade8aa3cf6-mis-viajes-v2.softwareseguro.com.ar"
UID = "ea42cd39-001b-4fb5-a509-449322674687"
URI = open("paisaje_datauri.txt").read().strip()

variants = [
    ("omit_user_id",   {"image": URI, "description": "v_omit"}),
    ("null_user_id",   {"image": URI, "description": "v_null", "user_id": None}),
    ("empty_user_id",  {"image": URI, "description": "v_empty", "user_id": ""}),
]
for label, body in variants:
    r = requests.post(f"{BASE}/upload", json=body)
    print(f"{label:16} -> {r.status_code}  body={r.text[:120].strip()}")

# does the listing now show these? read back and print rows whose desc starts with v_
r = requests.get(f"{BASE}/images/{UID}")
try:
    for img in r.json():
        if str(img.get("description","")).startswith("v_"):
            print("  mine:", img["id"], img["description"], img["filename"])
except Exception as e:
    print("readback err", e)
