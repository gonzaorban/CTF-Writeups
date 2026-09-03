cat << 'EOF' > /dev/shm/claude.py
import subprocess
import string
import time

binary = "/home/ctf-player/ad7e550b"
FLAG_LEN = 33
# Charset ordenado por probabilidad en flags CTF
CHARSET = "abcdefghijklmnopqrstuvwxyz0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ_!@#$%^&*-+="

flag = list("picoCTF{" + "A" * (FLAG_LEN - 9) + "}")

def contar_asteriscos(flag_list, timeout_seg=2.0):
    payload = "".join(flag_list)
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

print("[*] Iniciando timing attack por conteo de asteriscos...")
print(f"[*] Baseline con AAAA: {contar_asteriscos(flag)} asteriscos")

# Iteramos posición por posición desde índice 8 (después de "picoCTF{")
for i in range(8, FLAG_LEN - 1):
    mejor_char = flag[i]
    mejor_count = 0
    
    for c in CHARSET:
        flag[i] = c
        count = contar_asteriscos(flag, timeout_seg=2.0)
        
        if count > mejor_count:
            mejor_count = count
            mejor_char = c
            # Si encontramos más asteriscos que los anteriores, es correcto
            if count > i + 1:  # más asteriscos que la posición actual
                print(f"[+] [{i}] '{c}' -> {count} asteriscos ✓")
                break
        
        print(f"    [{i}] '{c}' -> {count}", end="\r")
    
    flag[i] = mejor_char
    print(f"\n[*] Flag parcial: {''.join(flag)}")

flag[FLAG_LEN - 1] = "}"
print(f"\n[!] FLAG FINAL: {''.join(flag)}")
EOF