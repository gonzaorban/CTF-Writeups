cat << 'PYEOF' > /dev/shm/diag.py
import subprocess, time, struct

binary = "/home/ctf-player/ad7e550b"
proc = subprocess.Popen([binary, "picoCTF{AAAAAAAAAAAAAAAAAAAAAAAA}"],
    stdout=subprocess.PIPE, stderr=subprocess.PIPE)
pid = proc.pid
print(f"[*] PID: {pid}")
time.sleep(3)

# Leer el mapa de memoria COMPLETO
with open(f"/proc/{pid}/maps") as f:
    maps_raw = f.read()

print("[*] MAPA COMPLETO:")
print(maps_raw)

# Parsear regiones válidas
regions = []
for line in maps_raw.strip().split('\n'):
    parts = line.split()
    start, end = [int(x, 16) for x in parts[0].split('-')]
    perms = parts[1]
    regions.append((start, end, perms))

def is_valid_addr(addr):
    for start, end, perms in regions:
        if start <= addr < end:
            return True, perms
    return False, None

def read_mem(addr, size):
    try:
        with open(f"/proc/{pid}/mem", "rb") as f:
            f.seek(addr)
            return f.read(size)
    except:
        return b''

base = regions[0][0]
print(f"[*] Base: 0x{base:x}")

# Verificar los primeros 3 punteros JIT
print("\n[*] Verificando punteros JIT:")
for i in range(3):
    raw = read_mem(base + 0x4120 + i * 8, 8)
    if len(raw) < 8:
        print(f"  JIT[{i}]: No se pudo leer el puntero")
        continue
    ptr = struct.unpack("<Q", raw)[0]
    valid, perms = is_valid_addr(ptr)
    print(f"  JIT[{i}]: ptr=0x{ptr:x} válido={valid} perms={perms}")
    if valid:
        code = read_mem(ptr, 20)
        print(f"    bytecode: {code.hex()}")

proc.kill()
PYEOF