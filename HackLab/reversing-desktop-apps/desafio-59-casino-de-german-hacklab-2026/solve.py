#!/usr/bin/env python3
"""
Solver del "Casino de Germán" (HackLab 2026).

El cliente (roulette.exe + random.dll) genera un `seed` y una lista de giros, y
los postea a https://ruleta.shared.softwareseguro.com.ar/verify. El servidor
RE-SIMULA la partida con ese mismo seed usando un LCG conocido (el que está en
random.dll) y, si el saldo final supera $1.000.000 de forma consistente, devuelve
la flag.

La falla: el `seed` lo elige el cliente y el PRNG es público (está en la DLL). Por
lo tanto se puede predecir el número de cada giro y fabricar un historial de
apuestas a pleno siempre ganadoras que el servidor validará como legítimo.

Detalle clave: random_init en la DLL hace `state = time() % 60` SOLO para la
animación local; el SERVIDOR usa el seed completo (sin %60). Esto se confirmó con
un dato real: seed 1791667440 -> salió el 9, que coincide con la fórmula de abajo.

Uso:
    python solve.py                 # imprime el JSON ganador
    python solve.py --seed 123456   # usa un seed concreto
    python solve.py --send          # lo postea con urllib y muestra la respuesta
"""
import argparse
import json
import time
import urllib.request

URL = "https://ruleta.shared.softwareseguro.com.ar/verify"

MASK = 0xFFFFFFFF
A = 0x41C64E6D   # multiplicador del LCG (1103515245)
C = 0x3039       # incremento del LCG (12345)
SALDO_INICIAL = 1000
OBJETIVO = 1_000_000
APUESTA_MAX = 10_000   # tope de $10.000 por tirada


def siguiente_numero(state):
    """Un paso del LCG tal como lo re-simula el servidor (seed completo, SIN %60)."""
    state = (state * A + C) & MASK
    numero = (state >> 16) % 37
    return state, numero


def generar_partida(seed):
    """Construye los giros apostando el máximo a pleno al número que va a salir."""
    state = seed & MASK
    saldo = SALDO_INICIAL
    spins = []
    while saldo < OBJETIVO:
        state, numero = siguiente_numero(state)
        apuesta = min(saldo, APUESTA_MAX)   # nunca apostar más que el saldo disponible
        spins.append([{"s": numero, "a": apuesta}])
        # pleno paga 35:1 -> recibís 36x lo apostado (devolución + premio)
        saldo = saldo - apuesta + apuesta * 36
    return {"seed": seed, "spins": spins}, saldo


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--seed", type=int, default=int(time.time()),
                    help="seed a usar (por defecto, el timestamp actual)")
    ap.add_argument("--send", action="store_true",
                    help="postear el JSON a /verify y mostrar la respuesta")
    args = ap.parse_args()

    payload, saldo = generar_partida(args.seed)
    print(f"[i] seed            = {payload['seed']}")
    print(f"[i] giros           = {len(payload['spins'])}")
    print(f"[i] saldo simulado  = ${saldo:,}")
    print(f"[i] números a pleno = {[g[0]['s'] for g in payload['spins']]}")
    body = json.dumps(payload)
    print("\n" + body)

    if args.send:
        req = urllib.request.Request(
            URL, data=body.encode(),
            headers={"Content-Type": "application/json", "User-Agent": "roulette/1.0"},
            method="POST",
        )
        with urllib.request.urlopen(req, timeout=10) as r:
            print("\n[>] respuesta del servidor:")
            print(r.read().decode())


if __name__ == "__main__":
    main()
