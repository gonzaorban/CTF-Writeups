# 🔢 Black Cobra Pepper

**Plataforma:** picoCTF  
**Categoría:** Criptografía  
**Vulnerabilidad:** Known-Plaintext Attack (KPA) / AES sin SubBytes (cifrado lineal)  
**Dificultad:** Media (200 Puntos)  

### 📂 Estructura de Archivos
* `chall.py`: Código fuente del algoritmo AES modificado provisto por el desafío.
* `output.txt`: Salida del programa — dos bloques cifrados (pt1 conocido + flag).
* `solve.py`: Script de explotación que recupera la flag usando un Known-Plaintext Attack.

---

### 1. Reconocimiento
Al descargar los archivos del desafío, encontramos un script Python (`chall.py`) que implementa una versión propia de AES-128. El programa cifra dos cosas con la misma key secreta y las imprime en `output.txt`:

1. Un plaintext **conocido**: `72616e646f6d64617461313131313131` (hardcodeado en el código fuente).
2. La **flag** (redactada en el código fuente).

El archivo `output.txt` nos provee ambos ciphertexts:
```
d7481d89f1aaf5a857f56edd2ae8994c   ← E(key, pt1)
8c7d66558130eb5796d131beb43c9934   ← E(key, flag)
```

---

### 2. Análisis de Vulnerabilidad
Analizando el código fuente, descubrimos que tres funciones críticas del algoritmo son **identidad** — es decir, no realizan ninguna operación:

```python
def sub_bytes(state):   return state   # ← debería aplicar la S-Box de AES
def sub_word(word):     return word    # ← debería aplicar S-Box al key schedule
def rcon(word):         return word    # ← debería XOR con la constante de ronda
```

En AES estándar, `SubBytes` es la **única operación no-lineal** del algoritmo. Al anularla, las operaciones restantes (ShiftRows, MixColumns, AddRoundKey) son todas transformaciones lineales sobre GF(2). Esto introduce una falla arquitectónica crítica:

* **El cifrado se vuelve completamente lineal**, lo que permite que un atacante con un solo par `(plaintext, ciphertext)` recupere cualquier otro plaintext sin conocer la key.
* **El key schedule también se debilita**, ya que `sub_word` y `rcon` son los responsables de introducir no-linealidad e independencia entre las round keys.

---

### 3. Explotación

La explotación se dividió en dos fases lógicas:

**Fase 1: Extracción de L(flag) mediante KPA**

Dado que el cifrado es lineal, cumple la siguiente propiedad:

```
E(key, A) XOR E(key, B)  =  E(key=0, A XOR B)
```

Teniendo `pt1` conocido y ambos ciphertexts, aplicamos:

```
c1 XOR c2  =  L(pt1) XOR L(flag)
```

Calculamos `L(pt1) = AES_encrypt(pt1, key=0)` — sin necesidad de la key secreta — y despejamos:

```
L(flag)  =  L(pt1) XOR c1 XOR c2
```

**Fase 2: Inversión algebraica**

Implementamos `AES_decrypt` invirtiendo cada operación del cifrado roto:
- `inv_shift_rows` — rota filas en dirección opuesta.
- `inv_mix_columns` — usa los coeficientes inversos `{0e, 0b, 0d, 09}` en GF(2⁸).
- `inv_sub_bytes` — identidad (igual que forward).

Aplicando el decrypt con `key=0` sobre `L(flag)` recuperamos la flag directamente:

```python
flag_hex = AES_decrypt(L_flag, "0" * 32)
flag = bytes.fromhex(flag_hex).decode("utf-8")
# → picoCTF{spi1cy!}
```

---

### 4. Resultado

Ejecutando `solve.py` obtenemos la flag sin necesidad de fuerza bruta ni conocer la key secreta:

```
=======================================================
  Known Plaintext Attack — Black Cobra Pepper CTF
=======================================================

[1] L(pt1)  = E(0, pt1)  = 539a3a3428c5cba8b46e2e2994cac001
[2] L(flag) = L(pt1) XOR c1 XOR c2 = 08af41e8585fd557754a714a0a1ec079
[3] flag (hex) = 7069636f4354467b737069316379217d

>>> FLAG: picoCTF{spi1cy!}
```

---

### 🛡️ Remediación (Developer Perspective)
Para evitar este tipo de vulnerabilidades en el diseño de sistemas criptográficos:

* **No reinventar la rueda criptográfica (Don't roll your own crypto):** Utilizar siempre implementaciones auditadas como `cryptography` o `PyCryptodome` en Python, que proveen AES-GCM o ChaCha20-Poly1305 correctamente implementados.
* **No omitir la S-Box:** `SubBytes` no es un detalle opcional — es el componente que garantiza la no-linealidad y la resistencia ante ataques algebraicos. Sin ella, AES se reduce a un sistema de ecuaciones lineales trivialmente resoluble.
* **Respetar los parámetros de diseño:** Todas las operaciones del estándar (SubBytes, Rcon, rondas completas) existen por razones matemáticas precisas. Alterar cualquiera puede colapsar la seguridad del esquema completo.