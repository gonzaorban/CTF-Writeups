cat << 'EOF' > /dev/shm/asteriscos2.py
import subprocess
import string
import sys

# Charset más probable para una flag picoCTF
CHARSET = string.ascii_lowercase + string.digits + "_{}"
FLAG_LEN = 33
TIMEOUT = 3  # segundos antes de cortar

known = list("picoCTF{" + "A" * (FLAG_LEN - 9) + "}")
# Ajustá los índices según lo que ya tengas

def try_char(flag_list):
    flag = "".join(flag_list)
    try:
        result = subprocess.run(
            ["./jitfp"],  # ajustá la ruta al binario
            input=flag + "\n",
            capture_output=True,
            text=True,
            timeout=TIMEOUT
        )
        output = result.stdout + result.stderr
    except subprocess.TimeoutExpired as e:
        # El timeout expiró: capturamos lo que salió hasta ese momento
        output = ""
        if e.stdout:
            output += e.stdout if isinstance(e.stdout, str) else e.stdout.decode(errors="replace")
        if e.stderr:
            output += e.stderr if isinstance(e.stderr, str) else e.stderr.decode(errors="replace")
    
    return output.count("*")

def solve():
    flag = list("picoCTF{" + "A" * (FLAG_LEN - 9) + "}")
    
    for i in range(8, FLAG_LEN - 1):  # saltamos "picoCTF{" y "}"
        best_char = flag[i]
        best_count = try_char(flag)
        
        print(f"[*] Posición {i}: baseline = {best_count} asteriscos")
        
        for c in CHARSET:
            flag[i] = c
            count = try_char(flag)
            print(f"    [{i}] '{c}' → {count} asteriscos", end="\r")
            
            if count > best_count:
                best_count = count
                best_char = c
                print(f"\n[+] Posición {i}: '{c}' da {count} asteriscos ✓")
                break  # encontramos uno mejor, siguiente posición
        
        flag[i] = best_char
        print(f"\n[+] Flag parcial: {''.join(flag)}")
    
    print(f"\n[!] Flag final: {''.join(flag)}")

solve()
EOF