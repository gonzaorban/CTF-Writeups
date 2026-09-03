# 🎯 Cifrado Oculto 1 (Hidden Cipher 1)

**Plataforma:** picoCTF
**Categoría:** Reverse Engineering
**Vulnerabilidad:** Binario Empaquetado (Packed Binary) / Hardcoded Key / Known-Plaintext Attack (KPA)
**Dificultad:** Media
**Herramientas:** UPX, `file`, Ghidra, Python, Netcat

### 📂 Estructura de Archivos
* `README.md`: Reporte detallado de la vulnerabilidad y explotación.
* `solve.py`: Script de Python utilizado para el ataque de texto plano conocido y el descifrado final.

---

### 1. Reconocimiento
Se nos proporciona un binario ELF. Al realizar el análisis inicial con el comando `file`, se observa que el ejecutable no posee cabeceras de sección (`no section header`) y figura como estáticamente enlazado. Estas son firmas clásicas de un binario comprimido u ofuscado mediante un *packer*.

Al conectarnos a la instancia remota vía Netcat (`nc candy-mountain.picoctf.net 55242`), el programa no solicita *input* interactivo, sino que imprime directamente un texto cifrado en formato hexadecimal: 
`235a201d702015483b1d412b265d3313501f0c072d135f0d2002302d01156a57224306172e`

### 2. Análisis de Vulnerabilidad
**Fase 1: Desempaquetado (Unpacking)**
Se procede a descomprimir el ejecutable utilizando UPX (`upx -d hiddencipher -o hiddencipher_unpacked`). El archivo resultante revela su verdadera estructura: un ELF de 64 bits, enlazado dinámicamente y, crucialmente, `not stripped`. Esto restaura la tabla de símbolos para el análisis estático.

**Fase 2: Análisis Estático**
Al auditar el binario limpio en Ghidra, se analiza la función `main`. Se identifica la lectura de un archivo local `flag.txt` y un bucle de cifrado:
```c
// Bucle extraído de Ghidra
for (local_2c = 0; (long)local_2c < (long)__n; local_2c = local_2c + 1) {
    printf("%02x",(ulong)(*(byte *)(lVar2 + local_2c % 6) ^ *(byte *)((long)__ptr + (long)local_2c)));
}
Hallazgos técnicos:El algoritmo de cifrado es un XOR bit a bit (^).La operación de módulo (local_2c % 6) sobre el puntero de la llave revela que la llave secreta tiene exactamente 6 caracteres de longitud.3. ExplotaciónDado que la llave está hardcodeada y el algoritmo es un XOR simétrico, se plantea un ataque de texto plano conocido (Known-Plaintext Attack). Sabiendo que todas las banderas comienzan con el formato estándar picoCT, podemos derivar la llave operando los primeros 6 bytes del texto cifrado contra este prefijo conocido.$Texto Cifrado \oplus Texto Claro = Llave$Al operar 235a201d7020 contra picoCT, se revela la llave estática: S3Cr3t.Con la llave en nuestro poder, se automatiza el proceso inverso mediante un script en Python para descifrar la cadena hexadecimal completa proporcionada por el servidor remoto.Script de Explotación (solve.py):Pythonciphertext_hex = "235a201d702015483b1d412b265d3313501f0c072d135f0d2002302d01156a57224306172e"
key = "S3Cr3t"
flag = ""

for i in range(len(ciphertext_hex) // 2):
    cipher_byte = int(ciphertext_hex[i*2 : i*2+2], 16)
    key_byte = ord(key[i % len(key)])
    flag += chr(cipher_byte ^ key_byte)

print(f"La flag descifrada es: {flag}")
4. ResultadoEl script procesa exitosamente la cadena generada dinámicamente por la instancia, revirtiendo la operación XOR y revelando el contenido original del archivo leido por el programa.Flag obtenida: picoCTF{xor_unpack_4nalys1s_2a9da15c}🛡️ Remediación (Developer Perspective)Para mitigar estas vulnerabilidades en el desarrollo de software seguro:Evitar Hardcoded Keys: Las llaves de cifrado o credenciales nunca deben estar incrustadas en el código fuente ni en los binarios compilados. Deben gestionarse mediante variables de entorno en tiempo de ejecución o servicios de gestión de claves (KMS/Vaults).Algoritmos Estándar: Evitar la creación de algoritmos criptográficos caseros ("Roll your own crypto"). En su lugar, utilizar bibliotecas probadas por la industria (ej. AES-GCM) que garantizan confidencialidad e integridad.