#!/usr/bin/env python3
"""
Respaldo Comprometido — crackeo offline del hash de 'admin'.

El backup filtrado (assets/usuarios.sql) guarda las contraseñas con sha512crypt
($6$), el mismo esquema que /etc/shadow. Se crackea por diccionario con passlib,
paralelizando entre los núcleos disponibles (sha512crypt en Python puro es lento).

Uso:
    pip install passlib
    python solve.py <wordlist.txt>
"""
import sys
import multiprocessing as mp
from passlib.hash import sha512_crypt

# Hash del usuario 'admin' extraído de assets/usuarios.sql
H = "$6$lab64adm$Guw66KEaFrRz0Itikk4AskR7aODQ/ZQ.nVlE.Wls5KIuyTu5abF.7I6oJENqCgtnvB1EsdUUDrGzqiP9zq0FU0"


def check(word):
    try:
        return word if sha512_crypt.verify(word, H) else None
    except Exception:
        return None


def main():
    if len(sys.argv) != 2:
        print(f"uso: {sys.argv[0]} <wordlist.txt>")
        sys.exit(1)
    words = [l.rstrip("\n\r") for l in open(sys.argv[1], encoding="latin-1") if l.strip()]
    print(f"[*] {len(words)} candidatos")
    with mp.Pool() as pool:
        for hit in pool.imap_unordered(check, words, chunksize=20):
            if hit is not None:
                print(f"[+] admin : {hit!r}")
                pool.terminate()
                return
    print("[-] sin match en el diccionario")


if __name__ == "__main__":
    main()
