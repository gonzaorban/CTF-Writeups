ciphertext_hex = "235a201d7020" # Los primeros 6 bytes de tu output
known_plaintext = "picoCT"

# Convertimos el hex a bytes y hacemos XOR con el texto conocido
key = ""
for i in range(len(known_plaintext)):
    cipher_byte = int(ciphertext_hex[i*2 : i*2+2], 16)
    plain_byte = ord(known_plaintext[i])
    key += chr(cipher_byte ^ plain_byte)

print(f"La llave secreta revelada es: {key}")