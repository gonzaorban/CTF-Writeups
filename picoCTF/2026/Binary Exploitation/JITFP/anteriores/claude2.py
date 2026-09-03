python3 /dev/shm/claude2.py

cat << 'EOF' > /dev/shm/claude2.py
import subprocess
import string

binary = "/home/ctf-player/ad7e550b"
FLAG_LEN = 33
CHARSET = "abcdefghijklmnopqrstuvwxyz0123456789_ABCDEFGHIJKLMNOPQRSTUVWXYZ"

def contar_asteriscos(payload, timeout_seg=3.0):
    # Verificación crítica: siempre 33 chars
    assert len(payload) == FLAG_LEN, f"ERROR: payload tiene {len(payload)} chars, necesita {FLAG_LEN}"
    try:
        proc = subprocess.Popen(
            [binary, payload],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )
        stdout, _ = proc.communicate(timeout=timeout_seg)
        return stdout.count(b'*')
    except subprocess.TimeoutExpired:
        proc.kill()
        stdout, _ = proc.communicate()
        return stdout.count(b'*')

# Verificación inicial
prefix = "picoCTF{"
suffix = "}"
# Los chars del medio son FLAG_LEN - len(prefix) - len(suffix) = 33 - 8 - 1 = 24
MIDDLE_LEN = FLAG_LEN - len(prefix) - len(suffix)  # = 24

test = prefix + "A" * MIDDLE_LEN + suffix
print(f"[*] Longitud de test: {len(test)}")  # debe ser 33
baseline = contar_asteriscos(test)
print(f"[*] Baseline (todo A): {baseline} asteriscos")

known_middle = ""

for i in range(MIDDLE_LEN):  # 0..23
    mejor_char = "A"
    mejor_count = -1

    for c in CHARSET:
        # Construimos: prefix + known + c + padding + suffix
        padding = "A" * (MIDDLE_LEN - len(known_middle) - 1)
        payload = prefix + known_middle + c + padding + suffix
        
        count = contar_asteriscos(payload)
        
        if count > mejor_count:
            mejor_count = count
            mejor_char = c

        print(f"    pos[{i+8}] '{c}' -> {count} *", end="\r")

    known_middle += mejor_char
    flag_parcial = prefix + known_middle + "A" * (MIDDLE_LEN - len(known_middle)) + suffix
    print(f"\n[+] pos[{i+8}] = '{mejor_char}' ({mejor_count}*) → {flag_parcial}")

print(f"\n[!] FLAG: {prefix + known_middle + suffix}")
EOF