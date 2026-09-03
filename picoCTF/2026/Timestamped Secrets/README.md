# 🎯 Secretos con marca de tiempo (Timestamped Secrets)

**Plataforma:** picoCTF
**Categoría:** Cryptography
**Vulnerabilidad:** Insecure Key Derivation (Time-based Seed) / Weak Entropy
**Dificultad:** Media (200 puntos)
**Herramientas:** Python, PyCryptodome

### 📂 Estructura de Archivos
* `README.md`: Reporte detallado de la vulnerabilidad y explotación.
* `solve.py`: Script utilizado para la automatización del ataque.
* `encryption.py`: Código fuente original del cifrado.
* `message.txt`: Archivo con el texto cifrado y la pista del timestamp.

---

### 1. Reconocimiento
El desafío entrega un script de cifrado (`encryption.py`) y un archivo de salida (`message.txt`). El código revela que el mensaje original fue cifrado usando el algoritmo AES en modo ECB. En el archivo de texto, el autor deja una pista vital: el timestamp (1770242628 UTC) en el que se realizó el cifrado aproximadamente, junto con el texto resultante en formato hexadecimal.

![Reconocimiento Inicial](./assets/01-recon.png)

### 2. Análisis de Vulnerabilidad
La vulnerabilidad crítica reside en la función `encrypt`, específicamente en cómo se genera la clave criptográfica. En lugar de utilizar una fuente de entropía segura (impredecible), la clave se deriva aplicando un hash SHA256 a la hora actual del sistema (`int(time.time())`) y truncando el resultado a 16 bytes.

Al basar la clave en un valor cronológico predecible, y al tener un conocimiento aproximado de cuándo se generó gracias al archivo `message.txt`, el espacio de claves se reduce drásticamente. En lugar de enfrentar $2^{128}$ combinaciones posibles para romper AES, el ataque se reduce a probar unos pocos números enteros correspondientes a los segundos cercanos a la marca de tiempo provista.

![Evidencia de la Vulnerabilidad](./assets/02-vulnerability.png)

### 3. Explotación
Se desarrolló un script de fuerza bruta en Python para barrer un rango de tiempo (+/- 2000 segundos) alrededor de la pista. El script recrea de manera idéntica la lógica vulnerable: convierte el entero a cadena, calcula su hash SHA256, toma los primeros 16 bytes e intenta descifrar el mensaje con AES-ECB.

**Payload utilizado (`solve.py`):**
```python
from hashlib import sha256
from Crypto.Cipher import AES

ciphertext = bytes.fromhex("2bcf79055a60b74654fada617a98a6f05bccbed9c2c9d74144f564fa699c6df3")
base_timestamp = 1770242628

for offset in range(-2000, 2000):
    test_timestamp = base_timestamp + offset
    key = sha256(str(test_timestamp).encode()).digest()[:16]
    cipher = AES.new(key, AES.MODE_ECB)
    
    try:
        pt = cipher.decrypt(ciphertext)
        if b"picoCTF{" in pt:
            flag = pt.decode('utf-8', 'ignore').strip()
            print(f"[🏆] Flag encontrada en timestamp {test_timestamp}: {flag[:flag.find('}')+1]}")
            break
    except Exception: pass
4. Resultado
El script rompió el cifrado instantáneamente. Se descubrió que el timestamp proporcionado en la pista (Offset: 0s) era el valor exacto utilizado para generar la clave, lo que permitió recuperar el texto plano de inmediato.

Flag: picoCTF{sa3S_sEc9t_9201873c}

🛡️ Remediación (Developer Perspective)
El uso de marcas de tiempo o cualquier otro dato predecible y público (como IDs secuenciales o nombres de usuario) como semilla para material criptográfico es una vulnerabilidad severa.

Uso de CSPRNGs: Para generar claves criptográficas fuertes, los desarrolladores deben utilizar Generadores de Números Pseudoaleatorios Criptográficamente Seguros (CSPRNG). En Python, se debe abandonar el uso de time.time() o el módulo estándar random para estos propósitos. En su lugar, se debe utilizar os.urandom(16) o la biblioteca moderna secrets (ej. secrets.token_bytes(16)), las cuales recopilan entropía real y segura del sistema operativo subyacente.