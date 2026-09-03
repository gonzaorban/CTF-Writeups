# ============================================================
# CTF: Black Cobra Pepper — picoCTF
# Categoría: Criptografía
# Técnica: Known Plaintext Attack sobre AES lineal (sin SubBytes)
# ============================================================

# ── Helpers ──────────────────────────────────────────────────

def xor_hex(a, b):
    """XOR de dos strings hexadecimales, devuelve hex string."""
    return bytes(x ^ y for x, y in zip(bytes.fromhex(a), bytes.fromhex(b))).hex()

def split(full_key):
    """Divide la key en 4 sub-keys intercaladas (como hace el código original)."""
    k = full_key
    sub_keys = ["", "", "", ""]
    for i in range(len(k)):
        sub_keys[i % 4] += k[0]
        k = k[1:]
    return sub_keys

def glue(parts):
    """Reensambla las 4 sub-keys en una sola key."""
    k = ""
    for i in range(32):
        k += parts[i % 4][0]
        parts[i % 4] = parts[i % 4][1:]
    return k

def rot_word(word):
    """Rota 1 byte hacia la izquierda (igual que el original)."""
    return str(word[2:]) + str(word[0:2])

def gen_keys(master_key):
    """Key schedule del AES roto (sin SubWord real ni Rcon real)."""
    keys = []
    k = master_key
    for _ in range(11):
        keys.append(k)
        sub_keys = split(k)
        sub_keys[-1] = rot_word(sub_keys[-1])
        # sub_word y rcon son identidad → se omiten
        sub_keys[0] = xor_hex(sub_keys[0], sub_keys[-1])
        sub_keys[1] = xor_hex(sub_keys[1], sub_keys[0])
        sub_keys[2] = xor_hex(sub_keys[2], sub_keys[1])
        sub_keys[3] = xor_hex(sub_keys[3], sub_keys[2])
        k = glue(sub_keys)
    return keys

# ── Operaciones de bloque ─────────────────────────────────────

def to_matrix(key):
    """Convierte 32 hex chars en matriz 4x4 (column-major, como AES)."""
    bytes_list = [int(key[i:i+2], 16) for i in range(0, 32, 2)]
    array = [[0] * 4 for _ in range(4)]
    for i in range(16):
        array[i % 4][i // 4] = hex(bytes_list[i])[2:]
    return array

def from_matrix(matrix):
    """Reconstruye hex string desde matriz 4x4 column-major."""
    r = ""
    for col in range(4):
        for row in range(4):
            r += matrix[row][col].zfill(2)
    return r

def shift_rows(state):
    """ShiftRows: rota cada fila i, i posiciones a la izquierda."""
    state[1][0], state[1][1], state[1][2], state[1][3] = state[1][1], state[1][2], state[1][3], state[1][0]
    state[2][0], state[2][1], state[2][2], state[2][3] = state[2][2], state[2][3], state[2][0], state[2][1]
    state[3][0], state[3][1], state[3][2], state[3][3] = state[3][3], state[3][0], state[3][1], state[3][2]
    return state

def inv_shift_rows(state):
    """InvShiftRows: inversa de shift_rows (rota a la derecha)."""
    state[1][0], state[1][1], state[1][2], state[1][3] = state[1][3], state[1][0], state[1][1], state[1][2]
    state[2][0], state[2][1], state[2][2], state[2][3] = state[2][2], state[2][3], state[2][0], state[2][1]
    state[3][0], state[3][1], state[3][2], state[3][3] = state[3][1], state[3][2], state[3][3], state[3][0]
    return state

def gmul(a, b):
    """Multiplicación en GF(2^8) — campo de Galois usado por AES."""
    if isinstance(b, str):
        b = int(b, 16)
    p = 0
    for _ in range(8):
        if b & 1:
            p ^= a
        a <<= 1
        if a & 0x100:
            a ^= 0x11b   # polinomio reductor de AES
        b >>= 1
    return p

def mix_columns(s):
    """MixColumns: mezcla columnas con la matriz de AES."""
    ss = [[0] * 4 for _ in range(4)]
    for c in range(4):
        ss[0][c] = hex(gmul(0x02, s[0][c]) ^ gmul(0x03, s[1][c]) ^ int(s[2][c], 16) ^ int(s[3][c], 16))[2:].zfill(2)
        ss[1][c] = hex(int(s[0][c], 16) ^ gmul(0x02, s[1][c]) ^ gmul(0x03, s[2][c]) ^ int(s[3][c], 16))[2:].zfill(2)
        ss[2][c] = hex(int(s[0][c], 16) ^ int(s[1][c], 16) ^ gmul(0x02, s[2][c]) ^ gmul(0x03, s[3][c]))[2:].zfill(2)
        ss[3][c] = hex(gmul(0x03, s[0][c]) ^ int(s[1][c], 16) ^ int(s[2][c], 16) ^ gmul(0x02, s[3][c]))[2:].zfill(2)
    for i in range(4):
        for j in range(4):
            s[i][j] = ss[i][j]
    return s

def inv_mix_columns(s):
    """InvMixColumns: inversa de mix_columns (usa coeficientes 0e, 0b, 0d, 09)."""
    ss = [[0] * 4 for _ in range(4)]
    for c in range(4):
        a0, a1, a2, a3 = int(s[0][c], 16), int(s[1][c], 16), int(s[2][c], 16), int(s[3][c], 16)
        ss[0][c] = hex(gmul(0x0e, a0) ^ gmul(0x0b, a1) ^ gmul(0x0d, a2) ^ gmul(0x09, a3))[2:].zfill(2)
        ss[1][c] = hex(gmul(0x09, a0) ^ gmul(0x0e, a1) ^ gmul(0x0b, a2) ^ gmul(0x0d, a3))[2:].zfill(2)
        ss[2][c] = hex(gmul(0x0d, a0) ^ gmul(0x09, a1) ^ gmul(0x0e, a2) ^ gmul(0x0b, a3))[2:].zfill(2)
        ss[3][c] = hex(gmul(0x0b, a0) ^ gmul(0x0d, a1) ^ gmul(0x09, a2) ^ gmul(0x0e, a3))[2:].zfill(2)
    for i in range(4):
        for j in range(4):
            s[i][j] = ss[i][j]
    return s

# ── AES encrypt / decrypt ─────────────────────────────────────

def AES_encrypt(plaintext, key):
    """AES roto (sin SubBytes ni Rcon real)."""
    round_keys = gen_keys(key)
    ct = xor_hex(round_keys[0], plaintext)
    for i in range(1, 10):
        ct = to_matrix(ct)
        shift_rows(ct)
        mix_columns(ct)
        ct = from_matrix(ct)
        ct = xor_hex(round_keys[i], ct)
    ct = to_matrix(ct)
    shift_rows(ct)
    ct = from_matrix(ct)
    ct = xor_hex(round_keys[10], ct)
    return ct

def AES_decrypt(ciphertext, key):
    """Inversa del AES roto."""
    round_keys = gen_keys(key)
    ct = xor_hex(round_keys[10], ciphertext)
    ct = to_matrix(ct)
    inv_shift_rows(ct)
    ct = from_matrix(ct)
    for i in range(9, 0, -1):
        ct = xor_hex(round_keys[i], ct)
        ct = to_matrix(ct)
        inv_mix_columns(ct)
        inv_shift_rows(ct)
        ct = from_matrix(ct)
    ct = xor_hex(round_keys[0], ct)
    return ct

# ── Ataque Known Plaintext ────────────────────────────────────

def solve():
    """
    Known Plaintext Attack sobre AES sin SubBytes.

    Sin SubBytes, el cifrado es LINEAL:
        E(K, A) XOR E(K, B)  =  E(key=0, A XOR B)

    Datos conocidos:
        pt1 = plaintext conocido del código fuente
        c1  = E(K, pt1)   ← output.txt línea 1
        c2  = E(K, flag)  ← output.txt línea 2

    Derivación:
        c1 XOR c2 = L(pt1) XOR L(flag)          [por linealidad]
        L(flag)   = L(pt1) XOR c1 XOR c2
        flag      = L_inv(L(flag))               [decrypt con key=0]
    """

    pt1 = "72616e646f6d64617461313131313131"   # del código fuente
    c1  = "d7481d89f1aaf5a857f56edd2ae8994c"   # output.txt línea 1
    c2  = "8c7d66558130eb5796d131beb43c9934"   # output.txt línea 2

    ZERO_KEY = "0" * 32   # key = 0x00...00

    print("=" * 55)
    print("  Known Plaintext Attack — Black Cobra Pepper CTF")
    print("=" * 55)

    # Paso 1: calcular L(pt1) = E(key=0, pt1)
    L_pt1 = AES_encrypt(pt1, ZERO_KEY)
    print(f"\n[1] L(pt1)  = E(0, pt1)  = {L_pt1}")

    # Paso 2: L(flag) = L(pt1) XOR c1 XOR c2
    L_flag = xor_hex(L_pt1, xor_hex(c1, c2))
    print(f"[2] L(flag) = L(pt1) XOR c1 XOR c2 = {L_flag}")

    # Paso 3: flag = L_inv(L(flag)) = AES_decrypt(key=0, L(flag))
    flag_hex = AES_decrypt(L_flag, ZERO_KEY)
    flag = bytes.fromhex(flag_hex).decode("utf-8")

    print(f"[3] flag (hex) = {flag_hex}")
    print(f"\n>>> FLAG: {flag}\n")
    return flag

if __name__ == "__main__":
    solve()