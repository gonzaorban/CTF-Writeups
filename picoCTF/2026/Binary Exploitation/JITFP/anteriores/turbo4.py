python3 /dev/shm/turbo4.py

cat << 'EOF' > /dev/shm/turbo4.py
import subprocess
import string
import time
from concurrent.futures import ThreadPoolExecutor

binary = "./ad7e550b"
# Alfabeto optimizado (picoCTF suele usar letras, numeros y guiones bajos)
alphabet = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789_"
flag = "picoCTF{"
target_len = 33

def measure_time(char):
    # Armamos la estructura perfecta: picoCTF{ + char + relleno + }
    # Esto garantiza 33 caracteres exactos y evita el Segfault
    pad_length = target_len - len(flag) - 2 # -1 por el char, -1 por la '}'
    test_payload = flag + char + ("A" * pad_length) + "}"
    
    start = time.perf_counter()
    # Ejecucion COMPLETA. Esperamos los ~34 segundos naturales
    subprocess.run([binary, test_payload], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    end = time.perf_counter()
    
    duration = end - start
    return char, duration

print("[*] Iniciando Ataque de Tiempo de Ejecucion Completa (Pacemaker)...")
print("[*] Advertencia: Cada bloque tomara ~34 segundos en resolverse.")

while len(flag) < target_len - 1:
    results = []
    print(f"\n[*] Analizando posicion {len(flag) + 1}...")
    
    # 4 workers para evitar bloqueos del servidor
    with ThreadPoolExecutor(max_workers=4) as executor:
        futures = [executor.submit(measure_time, c) for c in alphabet]
        for future in futures:
            results.append(future.result())
            
    # Ordenamos de mayor a menor tiempo. La ejecucion JIT extra deberia
    # hacer que la letra correcta tarde una fraccion de segundo mas.
    results.sort(key=lambda x: x[1], reverse=True)
    
    best_char, best_time = results[0]
    flag += best_char
    
    print(f"[+] Top 3 tiempos:")
    for i in range(3):
        print(f"    - '{results[i][0]}': {results[i][1]:.5f}s")
        
    print(f"[!] Bandera parcial: {flag}")

flag += "}"
print(f"\n[🏆] FLAG EXTRAIDA: {flag}")
EOF