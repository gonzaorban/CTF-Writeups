from pwn import *

def djb2(data: bytes) -> int:
    h = 0x1505
    for byte in data:
        h = byte + h * 0x21
        h = h & 0xFFFFFFFFFFFFFFFF  # overflow de 64 bits como en C
    # Convertir a signed long como hace C
    if h >= 0x8000000000000000:
        h = h - 0x10000000000000000
    return h

host = "candy-mountain.picoctf.net"
port = 53823  # actualizá si cambia

r = remote(host, port)

r.recvuntil(b"Please set a password for your account:\r\n")
r.sendline(b"A")

r.recvuntil(b"How many bytes in length is your password?\r\n")
r.sendline(b"100")

r.recvuntil(b"You entered:")
r.recvline()
r.recvuntil(b"Your successfully stored password:\r\n")

memoria_filtrada = r.recvline().strip().decode().split()

# Extraemos bytes desde índice 60
hash_input = bytearray()
for numero_str in memoria_filtrada[60:]:
    numero = int(numero_str)
    if numero == 0:
        break
    if numero < 0:
        numero = 256 + numero
    hash_input.append(numero)

# El \0 está en índice 12, entonces solo usamos los primeros 12 bytes
hash_input = hash_input[:12]

log.info(f"Bytes para hashear: {hash_input}")
log.info(f"Como string: {hash_input.decode(errors='replace')}")

resultado = djb2(hash_input)
log.success(f"Hash calculado: {resultado}")

r.recvuntil(b"Enter your hash to access your account!\r\n")
r.sendline(str(resultado).encode())

r.interactive()