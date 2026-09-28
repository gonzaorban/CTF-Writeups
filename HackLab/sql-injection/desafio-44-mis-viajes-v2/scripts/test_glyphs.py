# test_glyphs.py — upload each quote-like glyph image and see how the OCR stored it.
# We want a glyph whose summary_ocr contains a straight ' (U+0027) between the x's,
# so we can build a real SQL quote the OCR reliably delivers.
import requests

BASE = "https://chl-f4e46c02-efed-4276-8edf-ffade8aa3cf6-mis-viajes-v2.softwareseguro.com.ar"
UID  = "ea42cd39-001b-4fb5-a509-449322674687"

names = ["g_apos", "g_rsquo", "g_lsquo", "g_prime", "g_back", "g_acute"]
for name in names:
    uri = open(name + "_datauri.txt").read().strip()
    r = requests.post(f"{BASE}/upload", json={"image": uri, "description": "GLY_" + name, "user_id": UID})
    print(f"{name:9} -> {r.status_code}")

data = requests.get(f"{BASE}/images/{UID}").json()
print("\n--- how OCR stored each glyph (looking for a straight quote) ---")
for img in data:
    d = img.get("description", "")
    if d.startswith("GLY_"):
        s = img.get("summary_ocr", "")
        has_quote = "'" in s
        print(f"{d:14} ocr={s!r}   has_straight_quote={has_quote}")
