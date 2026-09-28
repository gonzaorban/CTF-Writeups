# find_react_app.py — a React bundle (main.js) is served somewhere under /images/<uuid> or similar.
# The main app uses vanilla script.js + Leaflet, NOT React. So there may be a SECOND app/panel.
# Find the HTML page that loads this React main.js, and any API it calls.
import requests, re
BASE = "https://chl-f4e46c02-efed-4276-8edf-ffade8aa3cf6-mis-viajes-v2.softwareseguro.com.ar"
UID  = "ea42cd39-001b-4fb5-a509-449322674687"

# Candidate pages that might host the React app
pages = [
    "/admin", "/panel", "/dashboard", "/app", "/react", "/manage",
    f"/images/{UID}", "/images", "/view", "/gallery", "/index.html",
    "/admin/", "/panel/", "/static/index.html",
]
for p in pages:
    try:
        r = requests.get(BASE+p, timeout=10)
        body = r.text
        has_react = "main.js" in body or "root" in body or "react" in body.lower()
        marker = "  <<< loads main.js / react root" if ("main.js" in body) else ("  (mentions root/react)" if has_react else "")
        print(f"{p:26} -> {r.status_code} len={len(body)}{marker}")
        if "main.js" in body:
            open("react_host.html","w",encoding="utf-8").write(body)
            print("   >>> saved react_host.html")
    except Exception as e:
        print(f"{p} ERR {e}")

# Also look for the JS asset paths and any /api the bundle references
print("\n--- fetch main.js and grep for API endpoints / fetch calls / uuids ---")
for jp in [f"/images/{UID}/main.js", "/main.js", "/static/js/main.js", "/assets/main.js"]:
    try:
        r = requests.get(BASE+jp, timeout=10)
        if r.status_code==200 and len(r.text)>1000:
            js = r.text
            print(f"got {jp} ({len(js)} bytes)")
            # find fetch/axios URLs and api paths
            for pat in [r'fetch\(["\`]([^"\`]+)', r'["\`](/api/[^"\`]+)', r'["\`](/images/[^"\`]*)', r'axios\.[a-z]+\(["\`]([^"\`]+)']:
                for m in set(re.findall(pat, js))[:20] if isinstance(set(re.findall(pat, js)), set) else []:
                    print("   endpoint:", m)
            for m in set(re.findall(r"[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}", js)):
                if m != UID:
                    print("   UUID:", m)
            break
    except Exception as e:
        print(jp, "ERR", e)
