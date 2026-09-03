cat << 'EOF' > /dev/shm/turbo.py
import subprocess
import string
import time
from concurrent.futures import ThreadPoolExecutor

binary = "./ad7e550b"
# Alfabeto reducido para ganar velocidad
alphabet = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ_{}"
flag = "picoCTF{" 
target_len = 33

def check_char(char, current_flag):
    # Padding de 33 chars para evitar el Segfault que vimos en Docker
    test_payload = current_flag + char + "A" * (target_len - len(current_flag) - 1)
    
    start = time.perf_counter()
    subprocess.run([binary, test_payload], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    end = time.perf_counter()
    
    return char, end - start

print(f"[*] Iniciando Ataque de Tiempo Sigiloso (4 hilos)...")

while len(flag) < target_len:
    results = []
    print(f"[*] Buscando caracter {len(flag)+1}...")
    
    # Solo 4 hilos para no disparar el RuntimeError
    with ThreadPoolExecutor(max_workers=4) as executor:
        futures = [executor.submit(check_char, c, flag) for c in alphabet]
        for future in futures:
            results.append(future.result())
    
    # La pista dice que el tiempo no es optimo si fallas.
    # En este binario, el acierto suele ser ligeramente MAS RAPIDO o MAS LENTO.
    # Vamos a imprimir los top 3 para que vos elijas si el script se equivoca.
    results.sort(key=lambda x: x[1], reverse=True)
    
    best_char, best_time = results[0]
    flag += best_char
    print(f"[!] Ganador: '{best_char}' con {best_time:.5f}s -> {flag}")
    
    if best_char == "}": break

print(f"\n[🏆] RESULTADO: {flag}")
EOF