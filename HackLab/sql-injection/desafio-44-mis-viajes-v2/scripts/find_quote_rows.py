# find_quote_rows.py — list every row whose summary_ocr kept a single quote, so we can see
# in WHICH context the OCR actually delivers quotes (c2 did). That tells us how to shape a
# payload the OCR reads WITH its quotes intact.
import requests
BASE = "https://chl-f4e46c02-efed-4276-8edf-ffade8aa3cf6-mis-viajes-v2.softwareseguro.com.ar"
UID  = "ea42cd39-001b-4fb5-a509-449322674687"
data = requests.get(f"{BASE}/images/{UID}").json()
print("rows whose summary_ocr contains a quote:")
for img in data:
    s = str(img.get("summary_ocr",""))
    if "'" in s:
        print(f"  id={img['id']} desc={img.get('description')!r} ocr={s!r}")
print("\ntotal rows:", len(data))
