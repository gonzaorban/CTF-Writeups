# probe_defaults.py — the winning row may have been seeded with a default/empty/null user_id,
# or a non-random 'demo' uuid. Also test a couple structural UUIDs.
import requests
BASE = "https://chl-f4e46c02-efed-4276-8edf-ffade8aa3cf6-mis-viajes-v2.softwareseguro.com.ar"

# Flask <uuid> requires canonical uuid format, so empty/NULL can't be tested via GET path.
# But we CAN test likely seeded demo/admin uuids and version-1/nil variants.
cands = [
    "00000000-0000-0000-0000-000000000000",
    "ffffffff-ffff-ffff-ffff-ffffffffffff",
    # namespace/demo uuids frequently used as fixtures:
    "6ba7b810-9dad-11d1-80b4-00c04fd430c8",  # RFC4122 DNS namespace
    "6ba7b811-9dad-11d1-80b4-00c04fd430c8",
    "550e8400-e29b-41d4-a716-446655440000",  # the classic example uuid
    "123e4567-e89b-12d3-a456-426614174000",  # wikipedia example uuid
    "a1b2c3d4-e5f6-7890-abcd-ef1234567890",
    "deadbeef-0000-0000-0000-000000000000",
]
for u in cands:
    r = requests.get(f"{BASE}/images/{u}")
    b = r.text.strip()
    hit = "   <<<< HIT" if (r.status_code==200 and b not in ("[]","")) else ""
    print(f"{u} -> {r.status_code} len={len(b)}{hit}")
