#!/usr/bin/env python3
"""Desafío 51 - Imagen Perdida (HackLab).

AES-CTR sin nonce ni contador conocidos: se recupera el bloque contador
inicial con un ataque de texto plano conocido sobre el header del PNG.
"""
import hashlib

from Crypto.Cipher import AES
from Crypto.Util import Counter

KEY = bytes.fromhex("deb5a45546ad4c06280c655ae81d327c4a55b4eadf8b97aab5372586dc7dd7ec")
ENC = "assets/confidencial.png.enc"
OUT = "assets/confidencial.png"

# Firma PNG (8 bytes) + longitud y tipo del chunk IHDR (8 bytes): siempre iguales
PNG_HEADER = bytes.fromhex("89504e470d0a1a0a0000000d49484452")

c = open(ENC, "rb").read()

# CTR: C0 = P0 xor AES_K(ctr0)  =>  ctr0 = AES_K^-1(C0 xor P0)
keystream0 = bytes(a ^ b for a, b in zip(c[:16], PNG_HEADER))
ctr0 = AES.new(KEY, AES.MODE_ECB).decrypt(keystream0)
print("bloque contador inicial:", ctr0.hex())

counter = Counter.new(128, initial_value=int.from_bytes(ctr0, "big"))
plain = AES.new(KEY, AES.MODE_CTR, counter=counter).decrypt(c)
open(OUT, "wb").write(plain)

print("md5:", hashlib.md5(plain).hexdigest())
