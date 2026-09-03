cat << 'PYEOF' > /dev/shm/writeback.py
import subprocess, time, struct, sys

binary = "/home/ctf-player/ad7e550b"
dummy = "A" * 33  # 33 chars dummy que luego sobrescribimos

proc = subprocess.Popen([binary, dummy], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
pid = proc.pid
print(f"[*] PID: {pid}")

# Esperamos que el servicio escriba las funciones JIT (durante el primer sleep)
time.sleep(0.7)

# Leer mapa de memoria
with open(f"/proc/{pid}/maps") as f:
    maps_data = f.read()

lines = maps_data.strip().split('\n')
base = int(lines[0].split('-')[0], 16)
stack_line = [l for l in lines if 'stack' in l][0]
stack_start, stack_end = [int(x,16) for x in stack_line.split()[0].split('-')]
print(f"[*] Base: 0x{base:x}, Stack: 0x{stack_start:x}-0x{stack_end:x}")

def read_mem(addr, size):
    with open(f"/proc/{pid}/mem", "rb") as f:
        f.seek(addr)
        return f.read(size)

# Leer índices y chars JIT
indices_raw = read_mem(base + 0x4020, 33 * 4)
indices = list(struct.unpack("<" + "I" * 33, indices_raw))
print(f"[*] Indices: {indices}")

PATTERN = bytes([0x80, 0x7d, 0xfc])
chars = {}
for i in range(33):
    ptr_raw = read_mem(base + 0x4120 + i * 8, 8)
    ptr = struct.unpack("<Q", ptr_raw)[0]
    code = read_mem(ptr, 32)
    idx = code.find(PATTERN)
    if idx != -1:
        chars[i] = code[idx + 3]
        print(f"  JIT[{i}] → 0x{code[idx+3]:02x} ({chr(code[idx+3])})")

# Reconstruir el flag correcto para ESTE proceso
flag_bytes = bytearray(33)
for pos in range(33):
    jit_idx = indices[pos]
    flag_bytes[pos] = chars.get(jit_idx, ord('?'))

flag_str = flag_bytes.decode(errors='replace')
print(f"\n[*] Flag reconstruido: {flag_str}")

# Encontrar argv[1] en el stack y sobreescribirlo
stack_data = read_mem(stack_start, stack_end - stack_start)
dummy_bytes = dummy.encode()
# rfind para buscar desde el tope del stack (donde viven los args)
offset = stack_data.rfind(dummy_bytes)

if offset == -1:
    print("[!] No encontramos argv[1] en el stack!")
    proc.kill()
    sys.exit(1)

argv_addr = stack_start + offset
print(f"[*] argv[1] en stack: 0x{argv_addr:x}")

# Escribir el flag correcto en el mismo proceso
with open(f"/proc/{pid}/mem", "r+b") as f:
    f.seek(argv_addr)
    f.write(flag_bytes)

print(f"[*] Flag escrita en memoria del proceso!")
print(f"[*] Esperando resultado...\n")

try:
    stdout, stderr = proc.communicate(timeout=45)
    output = stdout.decode(errors='replace')
    print(f"[*] Output:\n{output}")
except subprocess.TimeoutExpired:
    proc.kill()
    stdout, _ = proc.communicate()
    print(f"[*] Output (timeout): {stdout.decode(errors='replace')}")
PYEOF