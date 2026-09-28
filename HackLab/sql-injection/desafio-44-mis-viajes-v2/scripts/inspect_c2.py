# inspect_c2.py — re-read the c2 row (the only 200) and inspect EXACTLY how OCR rendered
# the pipes and quotes, char by char. That tells us why it didn't execute.
import requests
BASE = "https://chl-f4e46c02-efed-4276-8edf-ffade8aa3cf6-mis-viajes-v2.softwareseguro.com.ar"
UID  = "ea42cd39-001b-4fb5-a509-449322674687"
data = requests.get(f"{BASE}/images/{UID}").json()
for img in data:
    if img.get("description")=="SW_c2":
        s = img.get("summary_ocr","")
        print("raw:", repr(s))
        print("chars:", [c for c in s])
        print("has '||':", "||" in s, " has '| |':", "| |" in s)
        break
else:
    print("SW_c2 not found; listing recent ocr values:")
    for img in data[-6:]:
        print(img.get("description"), repr(img.get("summary_ocr")))
