import requests
BASE = "https://chl-f4e46c02-efed-4276-8edf-ffade8aa3cf6-mis-viajes-v2.softwareseguro.com.ar"
UID  = "ea42cd39-001b-4fb5-a509-449322674687"
for label, f in [("quote1","quote1_datauri.txt"), ("quote2","quote2_datauri.txt")]:
    uri = open(f).read().strip()
    r = requests.post(f"{BASE}/upload", json={"image": uri, "description": label, "user_id": UID})
    print(f"upload {label} -> {r.status_code}")
data = requests.get(f"{BASE}/images/{UID}").json()
for img in data:
    if img.get("description") in ("quote1","quote2"):
        print(f"{img['description']}: {img.get('summary_ocr')!r}")
