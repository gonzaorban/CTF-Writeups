#!/usr/bin/env python3
"""
Cliente de resolucion para el desafio Tetris (HackLab 2025).

Reproduce el protocolo que usa el binario `client`:
  1. Conecta por TCP a tetris-server.shared.softwareseguro.com.ar:15452
  2. Envia el nombre del jugador: 30 bytes, UTF-8, recortado y rellenado con \\x00
  3. Envia bytes de puntaje (0..100 por byte segun el cliente original),
     respetando el rate limit de <= 4 envios por segundo (ventana de 1s).
  4. Lee todo lo que responde el server y busca un MD5 (32 hex) => el flag.

No inventa nada del protocolo: cada paso sale del bytecode desensamblado
del propio client.pyc.

Uso tipico:
    python solve_tetris.py --name gonza --target 40000

Para probar la hipotesis H2 (mandar un byte > 100, que el cliente original
topea pero quiza el server no valide):
    python solve_tetris.py --name gonza --target 40000 --per-byte 255
"""

import argparse
import re
import socket
import sys
import time
from collections import deque

# --- Constantes tomadas literalmente del client.pyc ---
SERVER_DOMAIN = "tetris-server.shared.softwareseguro.com.ar"
SERVER_PORT = 15452
NAME_BYTES = 30
MAX_SEND_PER_SEC = 4          # rate limit del cliente original
MD5_RE = re.compile(rb"\b[a-fA-F0-9]{32}\b")


def build_name_bytes(name: str) -> bytes:
    """Igual que el cliente: name.encode('utf-8')[:30].ljust(30, b'\\x00')."""
    return name.encode("utf-8")[:NAME_BYTES].ljust(NAME_BYTES, b"\x00")


class RateLimiter:
    """Replica _rate_limit_before_send: <= MAX_SEND_PER_SEC en ventana de 1s."""

    def __init__(self, max_per_sec=MAX_SEND_PER_SEC):
        self.max_per_sec = max_per_sec
        self.sent_times = deque()

    def wait(self):
        now = time.monotonic()
        while self.sent_times and now - self.sent_times[0] > 1.0:
            self.sent_times.popleft()
        if len(self.sent_times) < self.max_per_sec:
            return
        sleep_for = 1.0 - (now - self.sent_times[0]) + 0.005
        if sleep_for > 0:
            time.sleep(min(sleep_for, 0.2))
        # reintentar hasta que haya lugar en la ventana
        self.wait()

    def mark(self):
        self.sent_times.append(time.monotonic())


def solve(host, port, name, target, per_byte, ignore_rate, read_secs):
    per_byte = max(0, min(255, per_byte))
    n_bytes = (target + per_byte - 1) // per_byte  # techo
    print(f"[*] Conectando a {host}:{port} ...")
    sock = socket.create_connection((host, port), timeout=4)
    sock.settimeout(0.5)

    sock.sendall(build_name_bytes(name))
    print(f"[+] Nombre enviado: {name!r} ({NAME_BYTES} bytes)")
    print(f"[*] Objetivo {target} => {n_bytes} bytes de valor {per_byte} "
          f"(rate limit {'OFF' if ignore_rate else str(MAX_SEND_PER_SEC)+'/s'})")

    limiter = RateLimiter()
    buf = bytearray()
    flag = None

    def drain():
        """Lee lo que haya sin bloquear demasiado; guarda MD5 si aparece."""
        nonlocal flag
        try:
            while True:
                data = sock.recv(4096)
                if not data:
                    return False  # server cerro
                buf.extend(data)
                txt = data.decode("ascii", errors="replace").strip()
                if txt:
                    print(f"    <server> {txt}")
                m = MD5_RE.search(bytes(buf))
                if m:
                    flag = m.group().decode()
                    return True
        except socket.timeout:
            return None
        except OSError:
            return False

    sent_total = 0
    for i in range(n_bytes):
        if not ignore_rate:
            limiter.wait()
        try:
            sock.sendall(bytes([per_byte]))
        except OSError as e:
            print(f"[!] Error al enviar (byte {i}): {e}")
            break
        if not ignore_rate:
            limiter.mark()
        sent_total += per_byte
        if i % 20 == 0 or i == n_bytes - 1:
            print(f"    -> enviados {i+1}/{n_bytes} bytes (suma cliente ~{sent_total})")
        r = drain()
        if r is True:
            break
        if r is False:
            print("[!] El server cerro la conexion.")
            break

    if flag is None:
        # dar tiempo final a que el server responda GANASTE
        print(f"[*] Esperando respuesta final ({read_secs}s) ...")
        end = time.monotonic() + read_secs
        while time.monotonic() < end and flag is None:
            r = drain()
            if r is False:
                break

    try:
        sock.close()
    except OSError:
        pass

    print("-" * 50)
    if flag:
        print(f"[+] FLAG (MD5): {flag}")
    else:
        tail = bytes(buf[-200:]).decode("ascii", errors="replace")
        print("[-] No se encontro MD5. Ultimos bytes recibidos:")
        print(tail if tail.strip() else "    (nada)")
    return flag


def main():
    ap = argparse.ArgumentParser(description="Solver Tetris HackLab 2025")
    ap.add_argument("--host", default=SERVER_DOMAIN)
    ap.add_argument("--port", type=int, default=SERVER_PORT)
    ap.add_argument("--name", required=True, help="nombre del jugador (<=30 bytes)")
    ap.add_argument("--target", type=int, default=40000, help="puntaje objetivo")
    ap.add_argument("--per-byte", type=int, default=100,
                    help="valor por byte (cliente usa 100; probar 255 para H2)")
    ap.add_argument("--ignore-rate", action="store_true",
                    help="NO respetar el rate limit (probar si el server no lo aplica)")
    ap.add_argument("--read-secs", type=float, default=5.0,
                    help="segundos de espera final de respuesta")
    args = ap.parse_args()

    try:
        solve(args.host, args.port, args.name, args.target,
              args.per_byte, args.ignore_rate, args.read_secs)
    except KeyboardInterrupt:
        print("\n[!] Interrumpido.")
        sys.exit(1)
    except OSError as e:
        print(f"[!] Error de red: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
