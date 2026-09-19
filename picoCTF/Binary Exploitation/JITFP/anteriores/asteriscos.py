python3 /dev/shm/asteriscos.py

cat << 'EOF' > /dev/shm/asteriscos.py
import subprocess
import string

binary = "./ad7e550b"
alphabet = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ_!"
flag = "picoCTF{" 
target_len = 33

print("[*] Iniciando ataque de conteo de asteriscos...")

while len(flag) < target_len - 1:
    for char in alphabet:
        # Armamos el payload de 33 caracteres exactos
        # Ejemplo: picoCTF{a + AAAAAAAAAAAAAAAAAAAAAAA + }
        padding = "A" * (target_len - len(flag) - 2)
        test_payload = flag + char + padding + "}"
        
        try:
            # Ejecutamos con un timeout corto para no esperar los 34 seg
            proc = subprocess.Popen([binary, test_payload], stdout=subprocess.PIPE, text=True)
            # Esperamos 1 segundo, suficiente para ver si sale un '*' extra
            stdout, _ = proc.communicate(timeout=1.0)
        except subprocess.TimeoutExpired:
            proc.kill()
            stdout, _ = proc.communicate()
        except:
            continue

        # El programa imprime asteriscos por cada letra correcta
        count = stdout.count('*')
        
        if count > len(flag):
            flag += char
            print(f"[+] Letra encontrada: {char} -> {flag}")
            break

flag += "}"
print(f"\n[🏆] FLAG FINAL: {flag}")
EOF