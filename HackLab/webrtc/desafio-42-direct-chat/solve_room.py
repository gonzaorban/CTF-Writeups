import base64
import hashlib
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend

# Room cifrada
encrypted_b64 = "PK8EdNdV53YOEsO6WGVFvw=="
ct = base64.b64decode(encrypted_b64)

# PBKDF2 HMAC-SHA256 con 'PIZZA', 1000 iteraciones, sin salt -> 48 bytes (32 key + 16 iv)
derived = hashlib.pbkdf2_hmac('sha256', b'PIZZA', b'', 1000, 48)
key = derived[:32]
iv = derived[32:48]

cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
decryptor = cipher.decryptor()
pt = decryptor.update(ct) + decryptor.finalize()

# Quitar padding PKCS7
pad_len = pt[-1]
room_name = pt[:-pad_len].decode('utf-8')

print(f"[+] Nombre de la room descifrada: {room_name}")
