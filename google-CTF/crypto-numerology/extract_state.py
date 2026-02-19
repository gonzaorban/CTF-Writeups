import json

# 1. Cargar el JSON que te trajo el reto
with open('ctf_challenge_package.json', 'r') as f:
    data = json.load(f)

# 2. Extraer los datos clave
key_hex = data['cipher_parameters']['key']
flag_ciphertext_hex = data['flag_ciphertext']
# El dataset de aprendizaje lo ignoramos por ahora, vamos directo a la yugular.

print(f"[*] Clave recuperada: {key_hex}")
print(f"[*] Longitud de la clave: {len(bytes.fromhex(key_hex))} bytes")
print(f"[*] Flag cifrada: {flag_ciphertext_hex}")

# Sabemos que la flag empieza con 'CTF{'
known_plaintext = b"CTF{"
flag_cipher_bytes = bytes.fromhex(flag_ciphertext_hex)

# Como el cifrado es un XOR, podemos sacar los primeros 4 bytes del keystream:
keystream_primeros_4_bytes = bytes([a ^ b for a, b in zip(known_plaintext, flag_cipher_bytes[:4])])
print(f"[*] Primeros 4 bytes del Keystream (Estado de salida 0): {keystream_primeros_4_bytes.hex()}")