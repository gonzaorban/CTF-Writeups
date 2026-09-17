from Crypto.Cipher import AES
import binascii

# ⚠️ IMPORTANTE: Rellené con dos '0' al final para llegar a los 64 bits. 
# Revisá el output.txt original para ver cuáles son los verdaderos.
initial_state = [0, 0, 1, 0, 0, 1, 0, 1, 1, 1, 1, 0, 1, 1, 0, 0, 1, 0, 0, 1, 0, 1, 1, 0, 1, 0, 0, 1, 0, 1, 0, 1, 0, 1, 0, 0, 1, 1, 0, 1, 1, 0, 0, 0, 1, 0, 1, 1, 1, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 1, 1, 0, 1, 1]
taps = [63, 61, 60, 58]

def clock_lfsr(state, taps):
    # Calculamos el bit de feedback aplicando XOR en las posiciones de los taps
    feedback = 0
    for t in taps:
        feedback ^= state[t]
    
    # El bit saliente usualmente es el último
    out_bit = state[-1]
    
    # Desplazamos el registro e insertamos el feedback al principio
    new_state = [feedback] + state[:-1]
    return new_state, out_bit

# Generamos 128 bits para la llave AES (16 bytes)
key_bits = []
state = initial_state.copy()
for _ in range(128):
    state, bit = clock_lfsr(state, taps)
    key_bits.append(bit)

# Convertimos los bits a bytes (asumiendo MSB)
key_bytes = bytearray()
for i in range(0, 128, 8):
    byte = 0
    for j in range(8):
        byte = (byte << 1) | key_bits[i+j]
    key_bytes.append(byte)

print(f"[*] Llave AES derivada (Hex): {key_bytes.hex()}")

# Intentamos desencriptar
ciphertext = bytes.fromhex("8f0e6d0f5b0dc1db201948b9e0cebd8f06069ee9ff30c87bd50b31d6fd72c4c438338e7e04fbddef0c6260a4eb758417")

try:
    # Usamos modo ECB ya que no nos dieron un Vector de Inicialización (IV)
    cipher = AES.new(key_bytes, AES.MODE_ECB)
    decrypted = cipher.decrypt(ciphertext)
    print(f"[🏆] Resultado: {decrypted}")
except Exception as e:
    print(f"[-] Error al desencriptar: {e}")