cat << 'EOF' > /dev/shm/script.py
import subprocess
import string
import time

binary = "./ad7e550b"
alphabet = "_" + string.ascii_letters + string.digits + "{}"
flag = "picoCTF{" 

print("[*] Iniciando Timing Attack optimizado...")

while not flag.endswith("}"):
    results = []
    for char in alphabet:
        test_payload = flag + char + "A" * (32 - len(flag))
        
        start = time.time()
        # Ejecutamos y esperamos a que termine o falle
        subprocess.run([binary, test_payload], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        end = time.time()
        
        duration = end - start
        results.append((char, duration))
        # Opcional: print(f"Probando {char}: {duration:.4f}s")

    # La letra correcta deberia ser la que mas tiempo (o menos, segun la penalizacion) tarda
    # Generalmente la que causa un ligero retraso extra
    results.sort(key=lambda x: x[1], reverse=True)
    best_char = results[0][0]
    flag += best_char
    print(f"[+] Flag parcial: {best_char} -> {flag}")
EOF