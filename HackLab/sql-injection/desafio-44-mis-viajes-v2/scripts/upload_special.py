import requests, json
BASE = "https://chl-f4e46c02-efed-4276-8edf-ffade8aa3cf6-mis-viajes-v2.softwareseguro.com.ar"
UID  = "ea42cd39-001b-4fb5-a509-449322674687"
uri = open("ocr_special_datauri.txt").read().strip()
r = requests.post(f"{BASE}/upload", json={"image": uri, "description": "ocr_special", "user_id": UID})
print("upload ->", r.status_code)
data = requests.get(f"{BASE}/images/{UID}").json()
for img in data:
    if img.get("description") == "ocr_special":
        print("wanted : '||()=SELECT-'")
        print("got    :", repr(img.get("summary_ocr")))
