# 🎯 cryptomaze

**Plataforma:** picoCTF
**Categoría:** Cryptography
**Vulnerabilidad:** Generador de Números Pseudoaleatorios Inseguro (LFSR)
**Dificultad:** Media (100 puntos)
**Herramientas:** Python, PyCryptodome

### 📂 Estructura de Archivos
* `README.md`: Reporte detallado de la vulnerabilidad y explotación.
* `script.py`: Script utilizado para la automatización y derivación de la llave.
* `output.txt`: Archivo original con el estado del registro y el texto cifrado.

---

### 1. Reconocimiento
El desafío proporciona un archivo `output.txt` que contiene información sobre la configuración criptográfica utilizada: el estado inicial de un Linear Feedback Shift Register (LFSR) compuesto por ceros y unos, una lista de "taps" (posiciones de retroalimentación) y una cadena hexadecimal que representa el mensaje encriptado con AES. El objetivo es derivar la llave AES de 128 bits reconstruyendo matemáticamente el estado del registro.

![Reconocimiento Inicial](./assets/01-recon.png)

### 2. Análisis de Vulnerabilidad
La vulnerabilidad central es el uso de un **LFSR para generar material criptográfico**. Los LFSR son secuencias lineales, deterministas y altamente predecibles; no poseen entropía real. Si se conoce el estado inicial y la disposición de los taps, cualquier atacante puede calcular el flujo exacto de bits (keystream) simulando los desplazamientos matemáticamente, rompiendo así por completo la seguridad de AES, ya que la llave en sí misma es deducible.

![Evidencia de la Vulnerabilidad](./assets/02-vulnerability.png)

### 3. Explotación
La explotación se automatizó mediante un script en Python. Dado que no había una convención explícita sobre la orientación del registro (dirección del shift, extracción de bits y Endianness), se diseñó un ataque de fuerza bruta sobre las configuraciones del hardware lógico. El LFSR se iteró 128 veces para capturar la cantidad de bits necesarios para una llave AES estándar.

**Payload utilizado (`script.py`):**
```python
import binascii
from Crypto.Cipher import AES

# Se agregaron dos ceros al estado inicial de 62 bits entregado para coincidir con el tap 63
initial_state = [0, 0, 1, 0, 0, 1, 0, 1, 1, 1, 1, 0, 1, 1, 0, 0, 1, 0, 0, 1, 0, 1, 1, 0, 1, 0, 0, 1, 0, 1, 0, 1, 0, 1, 0, 0, 1, 1, 0, 1, 1, 0, 0, 0, 1, 0, 1, 1, 1, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 1, 1, 0, 1, 1]
taps = [63, 61, 60, 58]
ciphertext = bytes.fromhex("8f0e6d0f5b0dc1db201948b9e0cebd8f06069ee9ff30c87bd50b31d6fd72c4c438338e7e04fbddef0c6260a4eb758417")

def bits_to_bytes(bits, endian='big'):
    res = bytearray()
    for i in range(0, len(bits), 8):
        chunk = bits[i:i+8]
        if endian == 'little':
            chunk = chunk[::-1]
        val = int("".join(map(str, chunk)), 2)
        res.append(val)
    return bytes(res)

for shift_dir in ['right', 'left']:
    for out_src in ['first', 'last', 'feedback']:
        for endian in ['big', 'little']:
            state = initial_state.copy()
            key_bits = []
            
            for _ in range(128):
                fb = 0
                for t in taps: fb ^= state[t]
                
                key_bits.append(state[0] if out_src == 'first' else state[-1] if out_src == 'last' else fb)
                state = [fb] + state[:-1] if shift_dir == 'right' else state[1:] + [fb]
            
            key = bits_to_bytes(key_bits, endian)
            try:
                pt = AES.new(key, AES.MODE_ECB).decrypt(ciphertext)
                if b'picoCTF' in pt: print(f"FLAG: {pt.decode('utf-8', 'ignore').strip()}")
            except Exception: pass
4. Resultado
El script reconstruyó exitosamente la secuencia del LFSR original, derivando la llave AES exacta en una de sus combinaciones lógicas. La desencriptación reveló la bandera en texto plano.

🛡️ Remediación (Developer Perspective)
Como buena práctica en ingeniería de software, utilizar estructuras predecibles (como un LFSR clásico) como generadores de claves anula la fortaleza de algoritmos robustos como AES. Para remediar esto:

Uso de CSPRNGs: Las llaves criptográficas deben generarse exclusivamente utilizando Generadores de Números Pseudoaleatorios Criptográficamente Seguros (CSPRNG), implementados a nivel del sistema operativo (por ejemplo, /dev/urandom en Linux) o mediante librerías comprobadas (como el módulo secrets en Python).

Funciones KDF: Si la llave AES requiere derivarse de otro material conocido, se debe utilizar una Función de Derivación de Llave (Key Derivation Function) estandarizada, como Argon2, PBKDF2 o HKDF, evitando implementaciones matemáticas lineales propias.