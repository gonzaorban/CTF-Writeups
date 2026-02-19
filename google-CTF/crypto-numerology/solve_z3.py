from z3 import *
import struct

def rotl32(v, c): return (v << c) | LShR(v, 32 - c)
def add32(a, b): return a + b

def mix_bits_z3(state, a_idx, b_idx, c_idx, d_idx):
    a, b, c, d = state[a_idx], state[b_idx], state[c_idx], state[d_idx]
    a = add32(a, b); d ^= a; d = rotl32(d, 16)
    c = add32(c, d); b ^= c; b = rotl32(b, 12)
    a = add32(a, b); d ^= a; d = rotl32(d, 8)
    c = add32(c, d); b ^= c; b = rotl32(b, 7)
    state[a_idx], state[b_idx], state[c_idx], state[d_idx] = a, b, c, d

solver = Solver()
counter = BitVec('counter', 32)
nonce0 = BitVec('nonce0', 32) # Lo dejamos para que no rompa las variables, aunque no se use

initial_state = [BitVecVal(0, 32) for _ in range(16)]
initial_state[5] = BitVecVal(0x0270545c, 32)
initial_state[7] = BitVecVal(0x7b72f431, 32)
initial_state[8] = BitVecVal(0x3492d4f7, 32)
initial_state[10] = BitVecVal(0xc9b1bbe7, 32)
initial_state[12] = counter
initial_state[13] = nonce0

state = initial_state[:]

# EL FIX: Solo se ejecuta la Ronda 1. 
mix_bits_z3(state, 0, 4, 8, 12)
# mix_bits_z3(state, 1, 5, 9, 13) <-- ESTA LÍNEA ERA LA CULPABLE

out_state = [add32(state[i], initial_state[i]) for i in range(16)]

# Nuestra única restricción real: el primer bloque coincide con 'CTF{'
solver.add(out_state[0] == 0x9d4f7b2a)
solver.add((nonce0 & 0x0000FFFF) == 0)

print("[*] Z3 está rompiendo el cifrado (Ronda 1)...")

if solver.check() == sat:
    m = solver.model()
    final_keystream = b""
    for i in range(11): 
        word_val = m.evaluate(out_state[i]).as_long()
        final_keystream += struct.pack("<I", word_val)

    ciphertext = bytes.fromhex("692f09e677335f6152655f67304e6e40141fa702e7e5b95b46756e63298d80a9bcbbd95465795f21ef0a")
    flag = bytes([a ^ b for a, b in zip(ciphertext, final_keystream)])
    print(f"\n[🏆] FLAG RECUPERADA: {flag.decode('utf-8', errors='ignore')}")
else:
    print("[-] UNSAT")