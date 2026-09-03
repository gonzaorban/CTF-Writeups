import binascii
from Crypto.Cipher import AES

initial_state = [0, 0, 1, 0, 0, 1, 0, 1, 1, 1, 1, 0, 1, 1, 0, 0, 1, 0, 0, 1, 0, 1, 1, 0, 1, 0, 0, 1, 0, 1, 0, 1, 0, 1, 0, 0, 1, 1, 0, 1, 1, 0, 0, 0, 1, 0, 1, 1, 1, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 1, 1, 0, 1, 1]
taps = [63, 61, 60, 58]
ciphertext = bytes.fromhex("8f0e6d0f5b0dc1db201948b9e0cebd8f06069ee9ff30c87bd50b31d6fd72c4c438338e7e04fbddef0c6260a4eb758417")

def bits_to_bytes(bits, endian='big'):
    res = bytearray()
    for i in range(0, len(bits), 8):
        chunk = bits[i:i+8]
        if endian == 'little':
            chunk = chunk[::-1] # Invertimos el orden de los bits en el byte
        val = int("".join(map(str, chunk)), 2)
        res.append(val)
    return bytes(res)

print("[*] Iniciando ataque de fuerza bruta sobre las configuraciones del LFSR...")

found = False
# Probamos todas las combinaciones posibles
for shift_dir in ['right', 'left']:
    for out_src in ['first', 'last', 'feedback']:
        for endian in ['big', 'little']:
            
            state = initial_state.copy()
            key_bits = []
            
            # Generamos 128 bits para la llave AES
            for _ in range(128):
                # 1. Calculamos el feedback (XOR de los taps)
                fb = 0
                for t in taps:
                    fb ^= state[t]
                
                # 2. Extraemos el bit de salida según la variante
                if out_src == 'first':
                    key_bits.append(state[0])
                elif out_src == 'last':
                    key_bits.append(state[-1])
                else:
                    key_bits.append(fb)
                    
                # 3. Desplazamos el registro
                if shift_dir == 'right':
                    state = [fb] + state[:-1]
                else:
                    state = state[1:] + [fb]
            
            # Convertimos los bits a bytes
            key = bits_to_bytes(key_bits, endian)
            
            try:
                # Variante 1: Modo ECB (Electronic Codebook)
                cipher_ecb = AES.new(key, AES.MODE_ECB)
                pt_ecb = cipher_ecb.decrypt(ciphertext)
                if b'picoCTF' in pt_ecb:
                    print(f"\n[🏆] ¡BINGO! (Modo ECB)")
                    print(f"    - Shift: {shift_dir} | Bit salida: {out_src} | Endianness: {endian}")
                    print(f"    - Llave AES: {key.hex()}")
                    print(f"\n[🏁] FLAG: {pt_ecb.decode('utf-8', 'ignore').strip()}")
                    found = True
                    break
                
                # Variante 2: Modo CBC (Cipher Block Chaining) con IV nulo
                cipher_cbc = AES.new(key, AES.MODE_CBC, iv=b'\x00'*16)
                pt_cbc = cipher_cbc.decrypt(ciphertext)
                if b'picoCTF' in pt_cbc:
                    print(f"\n[🏆] ¡BINGO! (Modo CBC con IV nulo)")
                    print(f"    - Shift: {shift_dir} | Bit salida: {out_src} | Endianness: {endian}")
                    print(f"    - Llave AES: {key.hex()}")
                    print(f"\n[🏁] FLAG: {pt_cbc.decode('utf-8', 'ignore').strip()}")
                    found = True
                    break
            except Exception:
                pass
                
        if found: break
    if found: break

if not found:
    print("[-] No hubo suerte. Hay otra variación matemática oculta que nos estamos perdiendo.")