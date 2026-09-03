cat << 'PYEOF' > /dev/shm/getflag2.py
import subprocess, time, struct

binary = "/home/ctf-player/ad7e550b"
payload = "picoCTF{AAAAAAAAAAAAAAAAAAAAAAAA}"

proc = subprocess.Popen([binary, payload], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
pid = proc.pid
print(f"[*] PID: {pid}")
time.sleep(2.5)

with open(f"/proc/{pid}/maps", "r") as f:
    base = int(f.readline().split("-")[0], 16)
print(f"[*] Base: 0x{base:x}")

def read_mem(addr, size):
    with open(f"/proc/{pid}/mem", "rb") as f:
        f.seek(addr)
        return f.read(size)

# Leer índices
indices_raw = read_mem(base + 0x4020, 33 * 4)
indices = list(struct.unpack("<" + "I" * 33, indices_raw))
print(f"[*] Indices: {indices}")

# Leer chars buscando el patrón 80 7d fc XX
PATTERN = bytes([0x80, 0x7d, 0xfc])
chars = {}
for i in range(33):
    ptr_raw = read_mem(base + 0x4120 + i * 8, 8)
    ptr = struct.unpack("<Q", ptr_raw)[0]
    code = read_mem(ptr, 32)
    
    # Buscar patrón cmp byte [rbp-4], XX
    idx = code.find(PATTERN)
    if idx != -1 and idx + 3 < len(code):
        char_byte = code[idx + 3]
        chars[i] = chr(char_byte)
        print(f"  JIT[{i}] offset={idx+3} → 0x{char_byte:02x} ({chr(char_byte)})")
    else:
        print(f"  JIT[{i}] PATRON NO ENCONTRADO, dump: {code.hex()}")
        chars[i] = '?'

# Reconstruir flag
flag = ""
for pos in range(33):
    jit_idx = indices[pos]
    flag += chars.get(jit_idx, '?')

print(f"\n[!] FLAG: {flag}")

# Verificar con prefijo conocido
if flag.startswith("picoCTF{") and flag.endswith("}"):
    print("[+] FLAG VALIDA!")
else:
    print(f"[!] Prefijo obtenido: {flag[:8]} (esperado: picoCTF{{)")
    
proc.kill()
PYEOF
python3 /dev/shm/getflag2.py