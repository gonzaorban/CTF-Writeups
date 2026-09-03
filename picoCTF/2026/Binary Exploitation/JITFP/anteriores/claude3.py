python3 /dev/shm/getflag.py

cat << 'PYEOF' > /dev/shm/getflag.py
import subprocess, time, struct, sys

binary = "/home/ctf-player/ad7e550b"
payload = "picoCTF{AAAAAAAAAAAAAAAAAAAAAAAA}"

# Lanzar el binario
proc = subprocess.Popen([binary, payload], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
pid = proc.pid
print(f"[*] PID: {pid}")
time.sleep(2.5)

# Leer el mapa de memoria para obtener la base
with open(f"/proc/{pid}/maps", "r") as f:
    first_line = f.readline()
base = int(first_line.split("-")[0], 16)
print(f"[*] Base: 0x{base:x}")

mem_path = f"/proc/{pid}/mem"

def read_mem(addr, size):
    with open(mem_path, "rb") as f:
        f.seek(addr)
        return f.read(size)

# Leer los 33 índices desde DAT_00104020
indices_raw = read_mem(base + 0x4020, 33 * 4)
indices = list(struct.unpack("<" + "I" * 33, indices_raw))
print(f"[*] Índices: {indices}")

# Leer los 33 punteros JIT desde DAT_00104120
chars = []
for i in range(33):
    ptr_raw = read_mem(base + 0x4120 + i * 8, 8)
    ptr = struct.unpack("<Q", ptr_raw)[0]
    # El byte de comparación está en offset +12 de la función
    char_byte = read_mem(ptr + 12, 1)[0]
    chars.append(chr(char_byte))
    print(f"  JIT[{i}] = 0x{char_byte:02x} ({chr(char_byte)})")

# Reconstruir la flag
flag = ""
for pos in range(33):
    jit_idx = indices[pos]
    flag += chars[jit_idx]

print(f"\n[!] FLAG: {flag}")
proc.kill()
PYEOF
