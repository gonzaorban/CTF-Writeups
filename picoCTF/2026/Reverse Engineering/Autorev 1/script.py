from pwn import *
import binascii

# Conectarse al servidor (¡Asegurate de cambiar el puerto si se reinició la instancia!)
host = "mysterious-sea.picoctf.net"
port = 62667 

print("[+] Conectando al servidor...")
r = remote(host, port)

# Leer hasta la línea que dice "Here's the next binary in bytes:"
r.recvuntil(b"Here's the next binary in bytes:\n")

# Leer el binario hexadecimal (lee hasta el siguiente salto de línea)
hex_data = r.recvline().strip().decode('utf-8')

# Convertir de hexadecimal a bytes binarios reales
binary_data = binascii.unhexlify(hex_data)

# Guardar el binario para analizarlo
with open("binary_1", "wb") as f:
    f.write(binary_data)

print("[+] Primer binario extraído y guardado como 'binary_1'")

# Cerramos la conexión, solo queríamos robar uno de muestra
r.close()