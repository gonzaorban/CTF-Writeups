from pwn import *
import hashpumpy
from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad
import ast

puerto = 57632

# Desactivar logs molestos de pwntools
context.log_level = 'error'

def solve():
    while True:
        print("[*] Conectando al servidor para buscar un vector ideal (L=1)...")
        r = remote('lonely-island.picoctf.net', puerto)
        
        # Extraer Flag Encriptada
        r.recvuntil(b"IV: ")
        iv = bytes.fromhex(r.recvline().strip().decode())
        r.recvuntil(b"Ciphertext: ")
        ciphertext = bytes.fromhex(r.recvline().strip().decode())
        
        r.recvuntil(b"Here are the vectors I trust won't leak my key:\n")
        
        trusted = []
        for _ in range(5):
            line = r.recvline().strip().decode()
            if line:
                vec_str, hash_hex = ast.literal_eval(line)
                trusted.append((vec_str, hash_hex))
        
        # Buscar vector de longitud 1 que no sea 0
        target_vec = None
        target_hash = None
        for v, h in trusted:
            if len(v) == 1 and v[0] != 0:
                target_vec = v
                target_hash = h
                break
        
        if target_vec is None:
            print("[-] No hubo suerte en esta instancia. Reconectando...")
            r.close()
            continue
            
        print(f"[+] ¡Jackpot! Vector confiable encontrado: {target_vec}")
        
        inner_str = str(target_vec)[1:-1]
        key = bytearray(32)
        
        print("[*] Extrayendo los 32 bytes de la clave AES...")
        # --- BYTE 0 ---
        payload = f"[{inner_str}]"
        r.recvuntil(b"Enter your vector: ")
        r.sendline(payload.encode())
        r.recvuntil(b"Enter its salted hash: ")
        r.sendline(target_hash.encode())
        
        r.recvuntil(b"The computed dot product is: ")
        d0 = int(r.recvline().strip().decode())
        
        v0 = int(inner_str.replace('-', '').strip())
        key[0] = d0 // v0
        
        # --- BYTES 1 al 31 ---
        for i in range(1, 32):
            append_str = ""
            for _ in range(i - 1):
                append_str += ", 0"
            append_str += ", 1"
            
            new_hash, new_inner = hashpumpy.hashpump(target_hash, inner_str.encode(), append_str.encode(), 256)
            
            payload = b"[" + new_inner + b"]"
            payload_escaped = payload.decode('latin-1').encode('unicode_escape')
            
            r.recvuntil(b"Enter your vector: ")
            r.sendline(payload_escaped)
            r.recvuntil(b"Enter its salted hash: ")
            r.sendline(new_hash.encode())
            
            r.recvuntil(b"The computed dot product is: ")
            di = int(r.recvline().strip().decode())
            
            key[i] = di - d0
            
        print(f"[+] ¡Clave AES extraída al 100%! -> {key.hex()}")
        
        # Desencriptar la bandera
        cipher = AES.new(bytes(key), AES.MODE_CBC, iv)
        flag = unpad(cipher.decrypt(ciphertext), AES.block_size)
        print(f"\n[🏆] BINGO: {flag.decode()}")
        r.close()
        break

if __name__ == "__main__":
    solve()