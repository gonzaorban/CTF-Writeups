# analyze_listing.py — carefully map ids to filenames in OUR listing and find the gaps.
# The global id sequence tells us which rows belong to OTHER users (the winner).
import requests, json
BASE = "https://chl-f4e46c02-efed-4276-8edf-ffade8aa3cf6-mis-viajes-v2.softwareseguro.com.ar"
UID = "ea42cd39-001b-4fb5-a509-449322674687"

data = requests.get(f"{BASE}/images/{UID}").json()
mine_ids = sorted(img["id"] for img in data)
print("my row ids:", mine_ids)
print("my max id:", max(mine_ids))
missing = [i for i in range(1, max(mine_ids)+1) if i not in mine_ids]
print("MISSING ids (belong to other users, incl. the winner):", missing)
print("\nmy filenames:")
for img in sorted(data, key=lambda x:x["id"]):
    print(f"  id={img['id']:3} {img['filename']}")
