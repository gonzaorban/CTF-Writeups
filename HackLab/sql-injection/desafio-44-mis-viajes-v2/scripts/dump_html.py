# dump_html.py — fetch the main page HTML and auto-extract every UUID and comment
import requests, re

BASE = "https://chl-f4e46c02-efed-4276-8edf-ffade8aa3cf6-mis-viajes-v2.softwareseguro.com.ar"
html = requests.get(BASE + "/").text
open("index_dump.html", "w", encoding="utf-8").write(html)
print("saved index_dump.html, len =", len(html))

uuids = set(re.findall(r"[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{12}", html))
print("\nUUIDs found in page:")
for u in uuids:
    print("  ", u)

comments = re.findall(r"<!--(.*?)-->", html, re.DOTALL)
print("\nHTML comments:")
for c in comments:
    print("  ", c.strip()[:200])

# also fetch the js it references and scan that too
for m in re.findall(r'src="([^"]+\.js)"', html):
    url = m if m.startswith("http") else BASE + ("" if m.startswith("/") else "/") + m
    try:
        js = requests.get(url).text
        print(f"\n--- {m} (len {len(js)}) UUIDs ---")
        for u in set(re.findall(r"[0-9a-fA-F-]{36}", js)):
            print("  ", u)
    except Exception as e:
        print("js fetch err", e)
