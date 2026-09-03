cat << 'EOF' > /dev/shm/exploit.py
import subprocess
import string
import time

# Usamos el binario original que ya esta en el servidor
binary = "./ad7e550b"
# Definimos el alfabeto de busqueda
alphabet = string.ascii_letters + string.digits + "_{}"
flag = "picoCTF{"

print("[*] Iniciando Side-Channel Attack en /dev/shm...")

while not flag.endswith("}"):
    for char in alphabet:
        test_payload = flag + char
        
        # Ejecutamos el binario original
        process = subprocess.Popen([binary, test_payload], 
                                 stdout=subprocess.PIPE, 
                                 stderr=subprocess.PIPE, 
                                 text=True)
        
        # El truco: esperamos solo 0.5 segundos. 
        # Si la letra es correcta, el asterisco aparece casi al instante.
        time.sleep(0.5)
        process.kill()
        stdout, _ = process.communicate()

        # Contamos los asteriscos que el programa alcanzo a escupir
        count = stdout.count('*')
        
        if count > len(flag):
            flag += char
            print(f"[+] Flag parcial: {flag}")
            break

print(f"\n[🏁] FLAG ENCONTRADA: {flag}")
EOF