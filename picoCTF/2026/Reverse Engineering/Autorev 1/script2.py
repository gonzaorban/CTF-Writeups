from pwn import *
import binascii
import subprocess
import re
import os

# ¡Acordate de chequear que el puerto sea el correcto!
HOST = "mysterious-sea.picoctf.net"
PORT = 62667 

def solve():
    r = remote(HOST, PORT)
    
    print(r.recvuntil(b"Here's the next binary in bytes:\n").decode())

    for i in range(20):
        log.info(f"Procesando binario {i+1}/20...")
        
        hex_data = r.recvline().strip().decode()
        
        with open("temp_bin", "wb") as f:
            f.write(binascii.unhexlify(hex_data))
        os.chmod("temp_bin", 0o777)
        
        dump = subprocess.check_output("objdump -d temp_bin", shell=True).decode()
        
        match = re.search(r'\$0x([0-9a-f]+),-0x4\(%rbp\)', dump)
        
        if not match:
            log.error("¡No se encontró el patrón!")
            break
            
        secret_hex = match.group(1)
        
        # CORRECCIÓN: Conversión directa a Unsigned Integer (Siempre positivo)
        secret_num = int(secret_hex, 16)
            
        log.success(f"Secreto encontrado: 0x{secret_hex} -> {secret_num}")
        
        try:
            # Enviamos la respuesta
            r.sendline(str(secret_num).encode())
            
            # Si no es el último, esperamos el siguiente prompt
            if i < 19:
                r.recvuntil(b"Here's the next binary in bytes:\n")
                
        except EOFError:
            log.error(f"¡El servidor cerró la conexión en el binario {i+1}!")
            # Imprimimos lo último que quedó en el buffer para ver por qué falló
            print(r.recvall(timeout=1).decode(errors='ignore'))
            break

    log.info("¡Ciclo completado! Esperando la bandera...")
    r.interactive()

if __name__ == "__main__":
    solve()