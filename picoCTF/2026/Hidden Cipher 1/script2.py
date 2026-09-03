ciphertext_hex = "235a201d702015483b1d412b265d3313501f0c072d135f0d2002302d01156a57224306172e"
key = "S3Cr3t"

flag = ""
# Procesamos el hexadecimal de a 2 caracteres (1 byte)
for i in range(len(ciphertext_hex) // 2):
    # Agarramos el byte cifrado actual
    cipher_byte = int(ciphertext_hex[i*2 : i*2+2], 16)
    # Agarramos el caracter correspondiente de la llave (usando el módulo 6)
    key_byte = ord(key[i % len(key)])
    # Hacemos el XOR mágico y lo convertimos a caracter
    flag += chr(cipher_byte ^ key_byte)

print(f"La flag descifrada es: {flag}")