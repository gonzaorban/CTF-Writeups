# run_calib.py — upload cal1..cal8, record status + delivered quote count.
# Builds the exact mapping: painted N -> delivered M (from summary_ocr) -> status (500/200).
import requests
BASE = "https://chl-f4e46c02-efed-4276-8edf-ffade8aa3cf6-mis-viajes-v2.softwareseguro.com.ar"
UID  = "ea42cd39-001b-4fb5-a509-449322674687"

status = {}
for n in range(1,9):
    uri = open(f"cal{n}_datauri.txt").read().strip()
    r = requests.post(f"{BASE}/upload", json={"image":uri,"description":f"CAL{n}","user_id":UID})
    status[n] = r.status_code

data = requests.get(f"{BASE}/images/{UID}").json()
delivered = {}
for img in data:
    d = img.get("description","")
    if d.startswith("CAL"):
        n = int(d[3:])
        delivered[n] = str(img.get("summary_ocr","")).count("'")

print("painted -> status -> delivered_quotes")
for n in range(1,9):
    print(f"  {n:2}  -> {status.get(n)} -> {delivered.get(n,'(500,no row)')}")
