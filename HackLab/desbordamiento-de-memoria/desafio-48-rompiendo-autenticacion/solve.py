#!/usr/bin/env python3
"""Solver del Desafío 48 - Rompiendo autenticación (HackLab).

El binario ELF guarda el mensaje de éxito ofuscado en la variable global
`success_msg_b64_enc` (64 bytes en .rodata). La función `decode_success_b64`
lo desofusca en dos pasos:

    1. XOR de cada byte con 0x23   (visto en el desensamblado: `xor eax, 0x23`)
    2. Base64 decode del resultado

No hace falta ejecutar el binario ni conocer la contraseña: basta con
replicar esos dos pasos sobre los bytes de la global para obtener el código.

Este script parsea el ELF a mano para localizar la global, así que funciona
sin objdump/readelf; solo necesita Python estándar.
"""
import base64
import struct
import sys

XOR_KEY = 0x23
GLOBAL_SYM = "success_msg_b64_enc"


def find_global_bytes(path):
    data = open(path, "rb").read()
    assert data[:4] == b"\x7fELF", "no es un ELF"

    e_shoff = struct.unpack_from("<Q", data, 0x28)[0]
    e_shentsize = struct.unpack_from("<H", data, 0x3A)[0]
    e_shnum = struct.unpack_from("<H", data, 0x3C)[0]
    e_shstrndx = struct.unpack_from("<H", data, 0x3E)[0]

    secs = []
    for i in range(e_shnum):
        off = e_shoff + i * e_shentsize
        keys = "name typ flags addr offset size link info align entsize".split()
        secs.append(dict(zip(keys, struct.unpack_from("<IIQQQQIIQQ", data, off))))

    shstr = secs[e_shstrndx]

    def cstr(base, off):
        end = data.index(b"\0", base + off)
        return data[base + off:end].decode()

    for s in secs:
        s["n"] = cstr(shstr["offset"], s["name"])
    byname = {s["n"]: s for s in secs}

    sym, strt = byname[".symtab"], byname[".strtab"]
    value = size = None
    for i in range(sym["size"] // sym["entsize"]):
        o = sym["offset"] + i * sym["entsize"]
        st_name, _, _, _, st_value, st_size = struct.unpack_from("<IBBHQQ", data, o)
        if cstr(strt["offset"], st_name) == GLOBAL_SYM:
            value, size = st_value, st_size
            break
    if value is None:
        raise SystemExit(f"no se encontró el símbolo {GLOBAL_SYM}")

    # sección que contiene la dirección de la global
    for s in secs:
        if s["addr"] and s["addr"] <= value < s["addr"] + s["size"]:
            file_off = s["offset"] + (value - s["addr"])
            return data[file_off:file_off + size]
    raise SystemExit("no se pudo mapear la dirección de la global a un offset de archivo")


def main():
    path = sys.argv[1] if len(sys.argv) > 1 else "assets/rompiendo-autenticacion.out"
    enc = find_global_bytes(path)

    b64 = bytes(b ^ XOR_KEY for b in enc)      # paso 1: XOR 0x23
    msg = base64.b64decode(b64).decode()       # paso 2: base64 decode

    print(f"[+] blob ofuscado ({len(enc)} bytes): {enc!r}")
    print(f"[+] tras XOR 0x23 (base64):          {b64.decode()}")
    print(f"[+] mensaje decodificado:            {msg}")

    codigo = msg.split(":", 1)[-1].strip()
    print(f"[+] CÓDIGO A ENVIAR:                 {codigo}")


if __name__ == "__main__":
    main()
