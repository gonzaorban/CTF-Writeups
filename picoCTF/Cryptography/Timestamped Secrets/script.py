from hashlib import sha256
from Crypto.Cipher import AES

# Los datos que sacamos de message.txt
ciphertext_hex = "2bcf79055a60b74654fada617a98a6f05bccbed9c2c9d74144f564fa699c6df3"
ciphertext = bytes.fromhex(ciphertext_hex)
base_timestamp = 1770242628

print("[*] Iniciando fuerza bruta del timestamp...")
print(f"[*] Buscando alrededor de {base_timestamp}...")

# Probamos +/- 2000 segundos alrededor de la pista
for offset in range(-2000, 2000):
    # Calculamos el timestamp a probar
    test_timestamp = base_timestamp + offset
    
    # Recreamos la logica de derivacion de clave
    key = sha256(str(test_timestamp).encode()).digest()[:16]
    
    # Inicializamos AES en modo ECB
    cipher = AES.new(key, AES.MODE_ECB)
    
    try:
        # Intentamos desencriptar
        pt = cipher.decrypt(ciphertext)
        
        # Si la frase picoCTF{ esta en el resultado, ganamos!
        if b"picoCTF{" in pt:
            print(f"\n[+] ¡Éxito! Timestamp real encontrado: {test_timestamp} (Offset: {offset}s)")
            
            # Limpiamos los bytes de padding al final
            flag = pt.decode('utf-8', 'ignore').strip()
            flag = flag[:flag.find('}')+1]
            
            print(f"[🏆] Bandera: {flag}")
            break
    except Exception:
        # Ignoramos errores de decodificacion de los intentos fallidos
        pass