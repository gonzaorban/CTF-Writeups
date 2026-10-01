#!/usr/bin/env python3
"""
Desafío 39 - El mejor secreto (HackLab 2025)

Recupera la contraseña de secreto.zip y descifra la flag, sin herramientas
externas: solo Python.

Modelo del problema
-------------------
El teclado numérico tiene teclas cuyo dígito real no coincide con la etiqueta
física. Lo único confiable del video son las POSICIONES pulsadas, y cada tecla
distinta corresponde a un dígito distinto (biyección desconocida).

La lectura del video fue, por posición de tecla:

    6A 6B 2 6B 9 6A 9 9 9 9 5 6B

...pero el tramo inicial estaba borroso: no quedaba claro el orden ni cuántas
pulsaciones había entre el 6A inicial y el primer 9. Por eso se enumeran a mano
las variantes plausibles de la secuencia completa (el resto, "9 6A 9 9 9 9 5 6B",
sí es claro), y para cada variante se prueban todas las asignaciones inyectivas
de teclas a dígitos, abriendo el zip con cada contraseña candidata.

El espacio total es de ~240 mil contraseñas: se resuelve en Python en segundos.
"""
import itertools
import hashlib
import hmac
import os
import zlib
from multiprocessing import Pool

ZIP = os.path.join(os.path.dirname(__file__), "assets", "secreto.zip")

# Tramo final claro de la secuencia (resto fijo).
RESTO = ["9", "6A", "9", "9", "9", "9", "5", "6B"]

# Variantes plausibles del tramo inicial borroso.
INICIOS = [
    ["6A", "6B", "2", "6B", "6B"],
    ["6A", "6B", "2", "2", "6B"],
    ["6A", "6B", "2", "6B", "2"],
    ["6A", "6B", "2", "2", "2"],
    ["6A", "2", "6B", "6B"],
    ["6A", "6B", "2", "6B"],
    ["6A", "2", "6B"],
    ["6A", "6B", "2"],
]
SECUENCIAS = [ini + RESTO for ini in INICIOS]


def leer_parametros_aes(path):
    """Extrae salt, verificador, ciphertext y authcode de un zip WinZip-AES."""
    data = open(path, "rb").read()
    fnlen = int.from_bytes(data[26:28], "little")
    eflen = int.from_bytes(data[28:30], "little")
    inicio = 30 + fnlen + eflen
    fin = data.find(b"PK\x07\x08", inicio)          # data descriptor
    if fin == -1:
        fin = data.find(b"PK\x01\x02", inicio)      # central directory
    blob = data[inicio:fin]
    salt = blob[:16]            # AES-256 -> salt de 16 bytes
    verificador = blob[16:18]   # 2 bytes de verificación de contraseña
    ciphertext = blob[18:-10]
    authcode = blob[-10:]       # HMAC-SHA1 truncado a 10 bytes
    return salt, verificador, ciphertext, authcode


# Parámetros del zip, cargados una sola vez por proceso.
SALT, VERIFICADOR, CIPHERTEXT, AUTHCODE = leer_parametros_aes(ZIP)


def probar(pw):
    """Devuelve (pw, flag) si pw es la contraseña correcta; si no, (pw, None)."""
    # Derivación WinZip-AES-256: 32 (clave) + 32 (mac) + 2 (verificador).
    dk = hashlib.pbkdf2_hmac("sha1", pw.encode(), SALT, 1000, 66)
    if dk[64:66] != VERIFICADOR:
        return (pw, None)
    # El verificador de 2 bytes puede colisionar; confirmar con el HMAC.
    if hmac.new(dk[32:64], CIPHERTEXT, hashlib.sha1).digest()[:10] != AUTHCODE:
        return (pw, None)
    # Contraseña correcta: descifrar (AES-CTR) e inflar (deflate).
    from Crypto.Cipher import AES
    from Crypto.Util import Counter
    ctr = Counter.new(128, initial_value=1, little_endian=True)
    raw = AES.new(dk[:32], AES.MODE_CTR, counter=ctr).decrypt(CIPHERTEXT)
    try:
        return (pw, zlib.decompress(raw, -15))
    except zlib.error:
        return (pw, raw)


def candidatos():
    vistos = set()
    for seq in SECUENCIAS:
        simbolos = sorted(set(seq))
        for perm in itertools.permutations("0123456789", len(simbolos)):
            mapping = dict(zip(simbolos, perm))
            pw = "".join(mapping[s] for s in seq)
            if pw in vistos:
                continue
            vistos.add(pw)
            yield pw


def main():
    with Pool() as pool:
        for pw, flag in pool.imap_unordered(probar, candidatos(), chunksize=500):
            if flag is not None:
                print(f"Contraseña : {pw}")
                print(f"Flag       : {flag.decode(errors='replace').strip()}")
                pool.terminate()
                return
    print("No encontrada.")


if __name__ == "__main__":
    main()
