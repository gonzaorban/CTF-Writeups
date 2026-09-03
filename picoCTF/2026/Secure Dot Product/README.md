# 🎯 Secure Dot Product

**Plataforma:** picoCTF
**Categoría:** Cryptography
**Vulnerabilidad:** Length Extension Attack (SHA-512) & Input Sanitization Flaw
**Dificultad:** Difícil (300 puntos)
**Herramientas:** Python, Pwntools, HashPump

### 📂 Estructura de Archivos
* `README.md`: Reporte detallado de la vulnerabilidad y explotación.
* `solve.py`: Script utilizado para interactuar con el socket y derivar la clave.
* `remote.py`: Código fuente del servidor vulnerable.

---

### 1. Reconocimiento
El desafío expone un servicio interactivo de álgebra lineal a través de un socket (`nc lonely-island.picoctf.net 56879`). El servidor calcula el producto punto entre una lista de enteros proporcionada por el usuario y una clave AES secreta de 32 bytes residente en memoria. Para aceptar el cálculo, el sistema exige un hash SHA-512 válido (con un `salt` secreto de 256 bytes). Al iniciar la conexión, el servidor amablemente proporciona 5 vectores de prueba generados aleatoriamente junto con sus hashes válidos. Además, nos entrega el IV y el texto cifrado (Ciphertext) de la bandera.

![Reconocimiento Inicial](./assets/01-recon.png)

### 2. Análisis de Vulnerabilidad
El servicio presenta dos debilidades críticas que, combinadas, permiten la extracción total de la clave:
1. **Length Extension Attack (LEA):** La función `hash_vector` implementa el hashing de manera insegura: `hashlib.sha512(self.salt + vector_encoding)`. Al colocar el secreto (sal) como prefijo en un algoritmo de la familia Merkle-Damgård (como SHA-512), un atacante puede tomar un hash legítimo conocido y calcular firmas válidas para datos adicionales concatenados al final, sin necesidad de conocer el contenido de la sal original.
2. **Deficiencia en la Sanitización de Inputs:** La función `parse_vector` purga cualquier carácter que no pertenezca a la lista permitida `'0123456789,[]'`. El ataque LEA inyecta "basura" binaria (como el padding obligatorio `\x80\x00...` y los metadatos de longitud de SHA-512) en medio de la cadena enviada. Al procesarse en el servidor, este filtro elimina todo el padding invisible malicioso sin arrojar errores de sintaxis. Esto deja un array de Python completamente válido, permitiéndonos anexar nuevos valores numéricos al vector original sin romper el formato.

![Evidencia de la Vulnerabilidad](./assets/02-vulnerability.png)

### 3. Explotación
El script `solve.py` automatiza la explotación utilizando la técnica de longitud unitaria ($L=1$):
* Se conecta reiteradamente al servidor hasta que este ofrece un vector confiable de un solo elemento (por ejemplo, `[220]`). Con un vector de un solo número, la matemática del producto punto se simplifica drásticamente.
* Se evalúa el vector base para aislar el primer byte de la clave ($k_0$): $k_0 = D_0 / v_0$.
* Se forjan iterativamente 31 firmas adicionales utilizando la librería `hashpumpy`, anexando secuencias como `", 0, 1"` al final del payload.
* Al limpiarse la basura binaria en el servidor, este procesa vectores progresivamente más largos (ej. `[220, 0, 1]`), lo que permite despejar matemáticamente cada byte subsiguiente de la clave AES restando el resultado anterior: $k_i = D_i - D_0$.

**Payload utilizado (`solve.py` - Fragmento del ataque de extensión):**
```python
# Iterar para extraer los bytes 1 a 31
for i in range(1, 32):
    append_str = ", 0" * (i - 1) + ", 1"
    new_hash, new_inner = hashpumpy.hashpump(target_hash, inner_str.encode(), append_str.encode(), 256)
    
    payload = b"[" + new_inner + b"]"
    # Se envía el payload y el nuevo hash al servidor...
4. Resultado
El script logró conectarse, identificar el vector ideal ([220]), inyectar el payload y reconstruir la clave AES completa byte por byte (d1815702cc46d4d3a2cc526b774b308377efc4524ee8b0b41df071e13da962aa). Utilizando esta clave y el IV inicial, se descifró la bandera correctamente.

Flag: picoCTF{n0t_so_s3cure_.x_w1th_sh@512_010e6475}

🛡️ Remediación (Developer Perspective)
Uso de HMAC para Autenticación de Mensajes: Jamás se debe construir firmas criptográficas mediante una simple concatenación como Hash(secret + message). Para proteger la integridad y autenticidad, se debe utilizar HMAC (Hash-based Message Authentication Code, ej. hmac.new(key, msg, hashlib.sha512)), el cual está diseñado específicamente para prevenir ataques de extensión de longitud mezclando la clave y el mensaje en múltiples pasos matemáticos seguros.

Deserialización Segura y Parsing Estricto: Depender de una limpieza manual de strings (eliminación de caracteres) antes de pasar los datos a un evaluador léxico (ast.literal_eval) es frágil. Si se espera una estructura de datos estandarizada, se debe utilizar un formato de intercambio robusto como JSON (json.loads()) y validar el esquema completo del input en lugar de intentar "arreglar" strings malformadas.