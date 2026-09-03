cat << 'EOF' > /dev/shm/final_solve.py
import subprocess
import string
import time

binary = "./ad7e550b"
# Alfabeto completo
alphabet = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ_}"
flag = "picoCTF{" 
target_len = 33

print("[*] Iniciando ataque de tiempo con Padding (Evitando Segfault)...")

while len(flag) < target_len:
    best_char = ""
    max_duration = 0
    
    for char in alphabet:
        # Relleno exacto para que el total sea siempre 33
        test_payload = flag + char + "A" * (target_len - len(flag) - 1)
        
        start = time.perf_counter()
        # Ejecutamos. No lo matamos, dejamos que el sleep(1) ocurra
        subprocess.run([binary, test_payload], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        end = time.perf_counter()
        
        duration = end - start
        
        # El acierto tardara notablemente mas (al menos 1 segundo mas)
        if duration > max_duration:
            max_duration = duration
            best_char = char
            
    flag += best_char
    print(f"[+] Caracter encontrado: {best_char} (Tiempo: {max_duration:.2f}s) -> {flag}")
    if best_char == "}": break

print(f"\n[🏆] FLAG: {flag}")
EOF