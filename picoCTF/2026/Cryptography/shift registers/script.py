# El texto cifrado que sacamos de output.txt
ct_hex = "21c1b705764e4bfdafd01e0bfdbc38d5eadf92991cdd347064e37444e517d661cea9"
ct_bytes = bytes.fromhex(ct_hex)

# La misma funcion del reto original
def steplfsr(lfsr):
    b7 = (lfsr >> 7) & 1
    b5 = (lfsr >> 5) & 1
    b4 = (lfsr >> 4) & 1
    b3 = (lfsr >> 3) & 1

    feedback = b7 ^ b5 ^ b4 ^ b3
    lfsr = (feedback << 7) | (lfsr >> 1)
    return lfsr

print("[*] Iniciando fuerza bruta sobre los 256 estados posibles...")

# Probamos todos los valores posibles para el byte inicial (0 a 255)
for initial_state in range(256):
    lfsr = initial_state
    pt_bytes = bytearray()
    
    # Desencriptamos byte por byte
    for c in ct_bytes:
        lfsr = steplfsr(lfsr)
        ks = lfsr
        # XOR para desencriptar
        pt_bytes.append(c ^ ks)
    
    # Comprobamos si el resultado tiene el formato de la flag
    if b"picoCTF{" in pt_bytes:
        print(f"[🏆] Flag encontrada con semilla {initial_state}:")
        print(pt_bytes.decode('utf-8', 'ignore'))
        break