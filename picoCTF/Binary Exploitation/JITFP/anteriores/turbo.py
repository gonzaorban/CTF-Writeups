cat << 'EOF' > /dev/shm/turbo.py
import subprocess
import string
import time
from concurrent.futures import ThreadPoolExecutor

binary = "./ad7e550b"
alphabet = "_" + string.ascii_letters + string.digits + "{}"
flag = "picoCTF{"
target_len = 33

def check_char(char, current_flag):
    test_payload = current_flag + char + "A" * (target_len - len(current_flag) - 1)
    start = time.time()
    # Ejecutamos y capturamos el tiempo exacto
    subprocess.run([binary, test_payload], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    end = time.time()
    return char, end - start

print(f"[*] Iniciando Multithreaded Timing Attack...")

while len(flag) < target_len:
    print(f"[*] Probando posición {len(flag) + 1}...")
    results = []
    
    # Lanzamos 50 hilos en paralelo (uno por cada caracter del alfabeto)
    with ThreadPoolExecutor(max_workers=50) as executor:
        futures = [executor.submit(check_char, c, flag) for c in alphabet]
        for future in futures:
            results.append(future.result())
    
    # Ordenamos por tiempo. Según la pista, el tiempo NO es óptimo si fallas.
    # Eso significa que la letra correcta tendrá un tiempo sutilmente diferente.
    # Probamos con la que tenga la mayor duración (debido al sleep extra).
    results.sort(key=lambda x: x[1], reverse=True)
    
    best_char, best_time = results[0]
    flag += best_char
    print(f"[!] Letra encontrada: '{best_char}' ({best_time:.4f}s) -> {flag}")
    
    if best_char == "}":
        break

print(f"\n[🏆] FLAG FINAL: {flag}")
EOF