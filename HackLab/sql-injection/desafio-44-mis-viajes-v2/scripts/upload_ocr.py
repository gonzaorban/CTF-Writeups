# upload_ocr.py — upload an image with visible text and see what lands in summary_ocr.
import requests, json
BASE = "https://chl-f4e46c02-efed-4276-8edf-ffade8aa3cf6-mis-viajes-v2.softwareseguro.com.ar"
UID  = "ea42cd39-001b-4fb5-a509-449322674687"

uri = open("ocr_control_datauri.txt").read().strip()
r = requests.post(f"{BASE}/upload", json={"image": uri, "description": "ocr_control", "user_id": UID})
print("upload ->", r.status_code, r.text[:80])

data = requests.get(f"{BASE}/images/{UID}").json()
for img in data:
    if img.get("description") == "ocr_control":
        print("summary_ocr =", repr(img.get("summary_ocr")))
        print("full row:", json.dumps({k:img[k] for k in ('id','make','model','summary_ocr')}, ensure_ascii=False))
