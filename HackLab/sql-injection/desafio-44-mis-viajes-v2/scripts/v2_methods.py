# v2_methods.py — POST /search etc gave 405 (Method Not Allowed) = the route EXISTS with some
# other method, while GET gave 404. Enumerate methods to find how to reach /search and friends.
# A 405 response's Allow header lists the accepted methods.
import requests

BASE = "https://chl-453bbf5a-0b09-4ad8-a4f2-61aeaba1384e-mis-viajes-v2.softwareseguro.com.ar"
paths = ["/search", "/images/search", "/api/search", "/upload", "/images"]
methods = ["GET","POST","PUT","DELETE","PATCH","OPTIONS","HEAD"]

for p in paths:
    print(f"\n=== {p} ===")
    for m in methods:
        try:
            r = requests.request(m, BASE+p, timeout=10)
            allow = r.headers.get("Allow","")
            extra = f"  Allow: {allow}" if allow else ""
            body = r.text[:50].replace("\n"," ")
            print(f"  {m:8} -> {r.status_code}{extra}")
        except Exception as e:
            print(f"  {m:8} ERR {e}")
