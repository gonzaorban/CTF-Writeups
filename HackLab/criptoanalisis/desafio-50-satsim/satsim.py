#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
SatSim - Generador de trama THRUSTER_FIRE
==========================================
El trafico esta cifrado con XOR usando un keystream de 16 bytes FIJO por bloque.
Cada bloque = 16 tramas (~2 min). El primer byte (prefijo) identifica el bloque.

Formato trama (16 bytes): [CMD_ID 2B][SEQ 2B][PAYLOAD 12B]
THRUSTER_FIRE = CMD_ID 0x0003, payload = [00*8][duration_ms 2B][delta_v 2B] (big-endian)
Objetivo: duration_ms > 2000 y delta_v > 50.

USO (super rapido)
------------------
1. En la web, selecciona las filas del bloque ACTIVO y copialas (Ctrl+C).
2. Pegalas TAL CUAL entre los triple-comillas de TRAFICO (abajo).
   No importa el formato: numero, hora, HEX y accion separados por tabs o espacios.
   El script encuentra el hex (32 caracteres) y la accion solo.
3. Corre:  python satsim.py
4. Copia la TRAMA generada y enviala YA (antes de que rote el bloque).

Necesitas AL MENOS UNA fila cuya accion sea un "ancla" (para descifrar el CMD):
   - "entra en modo seguro"                       -> SAFE_MODE      (0x0005)
   - "reorienta su cuerpo"                         -> SET_ATTITUDE   (0x0001)
   - "panel solar se despliega/retrae lentamente"  -> SOLAR_PANEL    (0x0002)
   - "apaga/enciende un instrumento de carga util" -> PAYLOAD_TOGGLE (0x0004)
   - "encendido de propulsores" (THRUSTER real)    -> THRUSTER       (0x0003)
"""

import re
from collections import Counter

# ---- Anclas: substring de la accion -> CMD_ID plano ----
# Verificadas en >=2 bloques descifrados. El KS_cmd_lo es constante por bloque, asi que
# CUALQUIERA de estas alcanza como ancla; con esta lista casi todo bloque tiene alguna.
ANCLAS = [
    # comandos documentados (5)
    ("entra en modo seguro",       0x0005),
    ("reorienta su cuerpo",        0x0001),
    ("panel solar se despliega",   0x0002),
    ("panel solar se retrae",      0x0002),
    ("apaga un instrumento",       0x0004),
    ("enciende un instrumento",    0x0004),
    ("encendido de propulsores",   0x0003),  # THRUSTER real
    # comandos extendidos (verificados en >=2 bloques)
    ("revision del estado de una bateria", 0x0007),
    ("camara de a bordo toma una fotografia", 0x0009),
    ("transmite un bloque de datos",       0x000a),
    ("subsistema se reinicia",             0x000b),
    ("antena principal se reorienta",      0x000c),
    ("rastreador de estrellas",            0x000f),
    ("vuelca un bloque de memoria",        0x0010),
    ("watchdog del satelite se reinicia",  0x0011),
    ("ajuste de orbita",                   0x0012),
    ("frecuencia del radio",               0x0013),
    ("frecuencia con la que se envia telemetria", 0x0014),
    ("cambia de modo de operacion",        0x0018),
    ("nivel de detalle de los registros",  0x0019),
    ("reconfigura un bus del sistema",     0x001a),
    ("limite termico",                     0x001b),
]

HEX32 = re.compile(r'\b([0-9a-fA-F]{32})\b')
NUMINI = re.compile(r'^\s*(\d+)\b')

def parsear(texto):
    """De texto crudo pegado saca [(frame_num, hex, accion), ...].
    frame_num = el numero de la 1a columna (contador global del sniffer)."""
    filas = []
    for linea in texto.strip().splitlines():
        m = HEX32.search(linea)
        if not m:
            continue
        h = m.group(1).lower()
        accion = linea[m.end():].strip()          # lo que viene DESPUES del hex
        mn = NUMINI.match(linea)
        num = int(mn.group(1)) if mn else None     # numero de fila (1a columna)
        filas.append((num, h, accion))
    return filas

def resolver(filas):
    """filas: [(frame_num, hex, accion), ...]"""
    Ball = [bytes.fromhex(h) for _, h, _ in filas]
    pref = Ball[0][0]
    keep = [(n, h, a, b) for (n, h, a), b in zip(filas, Ball) if b[0] == pref]
    nums   = [n for n, _, _, _ in keep]
    B      = [b for _, _, _, b in keep]
    frames = [(h, a) for _, h, a, _ in keep]

    KS = bytearray(16)
    KS[0] = pref                                   # cmd_hi (plano 00)
    for pos in range(4, 16):                        # keystream del payload
        KS[pos] = Counter(b[pos] for b in B).most_common(1)[0][0]

    ks_cmd_lo = None
    ancla_usada = None
    for (h, acc), b in zip(frames, B):
        al = acc.lower()
        for sub, cmd in ANCLAS:
            if sub in al:
                ks_cmd_lo = b[1] ^ (cmd & 0xFF)
                ancla_usada = (acc, cmd)
                break
        if ks_cmd_lo is not None:
            break
    if ks_cmd_lo is not None:
        KS[1] = ks_cmd_lo

    # ---- SEQ: contador GLOBAL cifrado con XOR (KS_seq constante en el bloque) ----
    # seq_plano = frame_num (el numero de la 1a columna del sniffer, contador que NUNCA
    # se reinicia). => KS_seq = seq_cif XOR frame_num, constante dentro del bloque.
    seq_cifs = [(b[2] << 8) | b[3] for b in B]
    ks_seq = None
    ultimo_frame = None
    if all(n is not None for n in nums):
        cand = {sc ^ n for sc, n in zip(seq_cifs, nums)}
        if len(cand) == 1:                          # KS_seq consistente => confirmado
            ks_seq = cand.pop()
            ultimo_frame = max(nums)
    if ks_seq is None:                              # fallback: sin numeros de fila fiables
        ks_seq = deducir_ks_seq(seq_cifs)
    KS[2], KS[3] = (ks_seq >> 8) & 0xFF, ks_seq & 0xFF
    return KS, ks_cmd_lo, pref, ancla_usada, B, ultimo_frame

def deducir_ks_seq(seq_cifs):
    """Fallback si no hay numeros de fila: KS_seq tal que los planos sean consecutivos."""
    for base in range(0, 256):
        ks = seq_cifs[0] ^ base
        planos = sorted(c ^ ks for c in seq_cifs)
        if len(set(planos)) == len(planos) and planos[-1] - planos[0] == len(planos) - 1:
            return ks
    return seq_cifs[0]

def construir(KS, ks_cmd_lo, next_counter, duration_ms=5000, delta_v=800):
    pay = [0]*8 + [(duration_ms >> 8) & 0xFF, duration_ms & 0xFF,
                   (delta_v >> 8) & 0xFF, delta_v & 0xFF]
    ks_seq = (KS[2] << 8) | KS[3]
    seq_cif = next_counter ^ ks_seq                # ciframos el contador nuevo
    out = bytearray(16)
    out[0] = 0x00 ^ KS[0]
    out[1] = 0x03 ^ ks_cmd_lo
    out[2] = (seq_cif >> 8) & 0xFF
    out[3] = seq_cif & 0xFF
    for i in range(12):
        out[4+i] = pay[i] ^ KS[4+i]
    return out.hex(), seq_cif

# ===================== PEGA EL TRAFICO AQUI =====================
# Copia las filas del bloque ACTIVO y pegalas tal cual (con una fila ancla).
TRAFICO = """
1	23:29:11	dc0789b133e7237e8c4ab2634c2ac13a	Se vuelca un bloque de memoria interna
2	23:29:21	dc0289b233e7237e8c4ab2639aa4c125	Se desactiva uno de los sensores del satélite
"""
DURATION_MS = 5000   # > 2000
DELTA_V     = 800    # > 50 (byte alto>0 = robusto ante el ultimo byte del keystream)
# ==============================================================

# MARGEN: cuantos frames por delante del ultimo visto mandar el SEQ.
# El sniffer va atrasado respecto al servidor. Subilo si dice "numero de secuencia
# incorrecto" (probar 2, 3, 5...). El SEQ es un contador GLOBAL basado en el numero
# de fila; enviamos frame_num_ultimo + MARGEN.
MARGEN = 2

if __name__ == "__main__":
    filas = parsear(TRAFICO)
    if len(filas) < 2:
        raise SystemExit("Pega al menos 2 tramas en TRAFICO (con una fila ancla).")
    KS, ks_cmd_lo, pref, ancla, B, ultimo_frame = resolver(filas)
    print(f"Bloque (prefijo): {pref:02x}   tramas usadas: {len(B)}")
    print(f"KS payload pos4..15: {bytes(KS[4:16]).hex()}")
    if ks_cmd_lo is None:
        print("\n!!! FALTA UN ANCLA. Agrega una fila cuya accion sea un comando conocido")
        print("    (modo seguro, reorienta cuerpo, panel despliega/retrae, instrumento,")
        print("     limite termico, revision bateria, reconfigura bus, watchdog, etc.)")
    elif ultimo_frame is None:
        print("\n!!! No pude leer el numero de fila (1a columna) o el SEQ no fue consistente.")
        print("    Pega las filas COMPLETAS con su numero al principio (ej: '227  23:22:27  36d6...').")
    else:
        ks_seq = (KS[2] << 8) | KS[3]
        print(f"KS_cmd_lo: {ks_cmd_lo:02x}  (ancla: {ancla[0]!r} = CMD {ancla[1]:04x})")
        print(f"KS_seq: {ks_seq:04x}  (contador GLOBAL = numero de fila)")
        nuevo = ultimo_frame + MARGEN
        print(f"ultimo frame visto: {ultimo_frame}  -> SEQ_plano a enviar: {nuevo} (MARGEN={MARGEN})")
        trama, seq_cif = construir(KS, ks_cmd_lo, nuevo, DURATION_MS, DELTA_V)
        print(f"\n>>> TRAMA THRUSTER_FIRE:  {trama}\n")
        b = bytes.fromhex(trama)
        cmd = (b[0] ^ KS[0]) << 8 | (b[1] ^ ks_cmd_lo)
        dur = (b[12] ^ KS[12]) << 8 | (b[13] ^ KS[13])
        p07 = bytes((b[4+i] ^ KS[4+i]) for i in range(8)).hex()
        print(f"    verifica: CMD={cmd:04x} SEQ_plano={nuevo} duration={dur} payload0-7={p07}")
        print(f"    delta_v>=768 garantizado (byte alto)")
        print(f"    Si dice 'numero de secuencia incorrecto': subi MARGEN o pega filas mas nuevas.")
