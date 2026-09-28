# probe_endpoints.py — discover extra endpoints beyond /images and /upload
import requests

BASE = "https://chl-f4e46c02-efed-4276-8edf-ffade8aa3cf6-mis-viajes-v2.softwareseguro.com.ar"

paths = [
    "/", "/users", "/user", "/api", "/api/users", "/api/images",
    "/images", "/admin", "/flag", "/debug", "/list",
    "/gallery", "/all", "/feed", "/public", "/uploads",
    "/static/script.js", "/robots.txt", "/.git/config",
    "/api/user", "/profile", "/me",
]
for p in paths:
    try:
        r = requests.get(BASE + p, timeout=10)
        print(f"{p:22} -> {r.status_code}  len={len(r.text)}  {r.text[:60].strip()!r}")
    except Exception as e:
        print(f"{p:22} -> ERR {e}")
