# 🔢 Crypto Numerology - Custom Cipher Challenge

**Plataforma:** Google CTF
**Categoría:** Criptografía / Ingeniería Inversa
**Dificultad:** Fácil (50 Puntos)

### 📂 Estructura de Archivos
* `crypto_numerology.py`: Código fuente decompilado del algoritmo original.
* `extract_state.py`: Script inicial para extraer el primer bloque del keystream (Ataque de Texto Plano Conocido).
* `solve_z3.py`: Solver algebraico que utiliza la librería Z3 para despejar las incógnitas y recuperar la flag.
* `ctf_challenge_package.json`: Paquete de datos crudos provisto por el reto.

### 1. Reconocimiento
Al descargar los archivos del desafío, nos encontramos con un entorno que contiene un script de inicialización (`init.sh`), un `readme.md`, una flag falsa para pruebas locales (`flag.txt`), un archivo `ctf_challenge_package.json` y el archivo más importante: `crypto_numerology.cpython-312.pyc` dentro de `__pycache__`.

Utilizando un decompilador online (pylingual.io), logramos revertir el bytecode de Python 3.12 a código fuente legible (guardado en este repositorio como `crypto_numerology.py`). El JSON adjunto nos proveía la clave pública estructurada y el texto cifrado (*ciphertext*) de la flag real.

### 2. Análisis de Vulnerabilidad
Analizando el código fuente decompilado, descubrimos que el autor intentó implementar su propio cifrado de flujo basándose en la función de mezcla matemática ("Quarter Round") del famoso algoritmo **ChaCha20**. 

Sin embargo, introdujo fallas arquitectónicas críticas:
* **Constantes Anuladas:** Las constantes mágicas de inicialización de ChaCha fueron sobrescritas con ceros (`struct.zeros = (0, 0, 0, 0)`).
* **Falta de Difusión (Rondas insuficientes):** En lugar de las 20 rondas estándar, el algoritmo se ejecutó con `--rounds 1`.
* Al ejecutar una sola ronda de mezcla (`mix_bits(s, 0, 4, 8, 12)`), las posiciones de la matriz que albergan el *Nonce* jamás llegan a procesarse. Además, gran parte de la matriz no muta, generando bloques de ceros en el *keystream* que filtran fragmentos del texto plano original en el texto cifrado.

### 3. Explotación
Para reflejar el proceso real de resolución, la explotación se dividió en dos fases lógicas:

**Fase 1: Extracción del Keystream (`extract_state.py`)**
Dado que conocemos el formato de la flag (`CTF{...`), realizamos un **Ataque de Texto Plano Conocido (Known-Plaintext Attack)**.
Al hacer XOR de los primeros 4 bytes del *ciphertext* contra los bytes de `CTF{`, recuperamos el primer bloque del *keystream* generado por el algoritmo (`0x9d4f7b2a`).

**Fase 2: Resolución Algebraica (`solve_z3.py`)**
Para evitar la fuerza bruta, desarrollamos un segundo script en Python utilizando **Z3 Theorem Prover**:
1. Replicamos la única operación de mezcla (`mix_bits`) en el solver.
2. Ingresamos el estado inicial usando la clave conocida extraída del JSON.
3. Establecimos como restricción que la salida de la primera palabra debía coincidir con el valor extraído en la Fase 1 (`0x9d4f7b2a`).
4. Le pedimos a Z3 que despejara matemáticamente la variable del `Counter` secreto.

### 4. Resultado
El solver Z3 resolvió el sistema de ecuaciones de manera instantánea, calculando el valor exacto del contador. Con este dato, el script generó el *keystream* completo válido. Al aplicar una operación XOR final entre este *keystream* y el *ciphertext* del JSON, el servidor local devolvió la flag correcta, completando el desafío.

### 🛡️ Remediación (Developer Perspective)
Para evitar este tipo de vulnerabilidades en el diseño de arquitecturas de software:
* **No reinventar la rueda criptográfica (Don't roll your own crypto):** Utilizar siempre implementaciones estándar, auditadas y provistas por librerías robustas del framework (por ejemplo, usar el módulo `crypto` nativo en NestJS/Node o la librería `cryptography` en Django/Python) para algoritmos como AES-GCM o ChaCha20-Poly1305.
* **Respetar los parámetros de diseño:** No alterar las constantes de inicialización (*nothing-up-my-sleeve numbers*) de un algoritmo, ya que garantizan la asimetría inicial de los datos.
* **Garantizar la difusión:** Asegurar que se ejecuten las rondas completas especificadas por el estándar matemático (ej. 20 rondas en ChaCha20) para que un ataque algebraico sea computacionalmente inviable.