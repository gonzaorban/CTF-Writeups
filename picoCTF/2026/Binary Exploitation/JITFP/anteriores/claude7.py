cat << 'PYEOF' > /dev/shm/getflag3.py
import subprocess, time, struct, sys

binary = "/home/ctf-player/ad7e550b"
dummy = "A" * 33
KNOWN_PREFIX = "picoCTF{"  # los primeros 8 chars que conocemos

proc = subprocess.Popen([binary, dummy], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
pid = proc.pid
print(f"[*] PID: {pid}")

# Esperamos más tiempo para que el servicio escriba TODAS las funciones
time.sleep(2.0)

with open(f"/proc/{pid}/maps") as f:
    base = int(f.readline().split("-")[0], 16)

def read_mem(addr, size):
    with open(f"/proc/{pid}/mem", "rb") as f:
        f.seek(addr)
        return f.read(size)

indices_raw = read_mem(base + 0x4020, 33 * 4)
indices = list(struct.unpack("<" + "I" * 33, indices_raw))

PATTERN = bytes([0x80, 0x7d, 0xfc])
chars = {}
for i in range(33):
    ptr_raw = read_mem(base + 0x4120 + i * 8, 8)
    ptr = struct.unpack("<Q", ptr_raw)[0]
    code = read_mem(ptr, 32)
    idx = code.find(PATTERN)
    if idx != -1:
        chars[i] = code[idx + 3]

# Verificar contra prefijo conocido
print("[*] Verificando prefijo conocido:")
ok = True
for pos, expected_char in enumerate(KNOWN_PREFIX):
    jit_idx = indices[pos]
    got = chars.get(jit_idx, 0)
    status = "✓" if got == ord(expected_char) else "✗"
    print(f"  pos[{pos}] JIT[{jit_idx}] = 0x{got:02x} ({chr(got)}) esperado '{expected_char}' {status}")
    if got != ord(expected_char):
        ok = False

if not ok:
    print("\n[!] El prefijo no coincide - JIT aún no inicializado o lectura incorrecta")
    print("[!] Aumentá el sleep y reintentá")
    proc.kill()
    sys.exit(1)

print("\n[+] Prefijo verificado correctamente!")

# Reconstruir flag completo
flag_bytes = bytearray(33)
for pos in range(33):
    jit_idx = indices[pos]
    flag_bytes[pos] = chars.get(jit_idx, ord('?'))

flag_str = flag_bytes.decode(errors='replace')
print(f"[+] Flag: {flag_str}")

# Escribir en memoria del proceso
stack_data = read_mem(
    int([l for l in open(f"/proc/{pid}/maps").readlines() if 'stack' in l][0].split('-')[0], 16),
    0x21000
)
offset = stack_data.rfind(dummy.encode())
if offset == -1:
    print("[!] argv[1] no encontrado en stack")
    proc.kill()
    sys.exit(1)

stack_start = int([l for l in open(f"/proc/{pid}/maps").readlines() if 'stack' in l][0].split('-')[0], 16)
argv_addr = stack_start + offset
print(f"[*] Escribiendo flag en 0x{argv_addr:x}...")

with open(f"/proc/{pid}/mem", "r+b") as f:
    f.seek(argv_addr)
    f.write(flag_bytes)

# Verificar que se escribió
verify = read_mem(argv_addr, 33)
if verify == bytes(flag_bytes):
    print("[+] Escritura verificada correctamente!")
else:
    print(f"[!] Escritura FALLÓ. Leído: {verify.hex()}")
    proc.kill()
    sys.exit(1)

print("[*] Esperando resultado del binario...\n")
try:
    stdout, _ = proc.communicate(timeout=45)
    print(stdout.decode(errors='replace'))
except subprocess.TimeoutExpired:
    proc.kill()
    stdout, _ = proc.communicate()
    print(stdout.decode(errors='replace'))
PYEOF