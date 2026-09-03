# 🎯 Binary Instrumentation 3

**Plataforma:** picoCTF
**Categoría:** Reverse Engineering / Malware Analysis
**Vulnerabilidad:** Flujo Lógico Roto / Reflective PE Loader / Obfuscation
**Dificultad:** Media/Alta (300 points)
**Herramientas:** Kali Linux, Ghidra, Python (`pefile`), `binwalk`, `lzma`, `base64`

### 📂 Estructura de Archivos
* `bin-ins.exe`: Binario original (Dropper/Loader) proporcionado por el reto.
* `extractor.py`: Script de Python desarrollado para dumpear las secciones PE.
* `seccion_.ATOM.bin`: Sección extraída que contiene el payload comprimido.
* `flag_generator.exe`: Binario final extraído y descomprimido.
* `README.md`: Reporte detallado del análisis y resolución.

---

### 1. Reconocimiento Inicial y Evasión de Antivirus
Al intentar interactuar con el archivo original en un entorno compartido con Windows, el antivirus (Avast) lo eliminó inmediatamente clasificándolo como `Win64:MalwareX-gen`. Esto es un claro indicador de técnicas de ofuscación o empaquetado malicioso. 

*[INSERTAR IMAGEN AQUÍ: Captura de la alerta de Avast moviendo el archivo a la cuarentena]*

Para realizar un análisis seguro (Cold Reverse Engineering), el binario fue aislado y analizado íntegramente desde la terminal de Kali Linux.
* **Comprobación de arquitectura:** El comando `file` confirmó que se trata de un ejecutable `PE32+ x86-64` de Windows.
* **Búsqueda de cadenas:** Un análisis inicial con `strings` no reveló ninguna bandera en texto plano, indicando que la misma se genera dinámicamente o está cifrada.

### 2. Análisis Estático (El Dropper)
Se importó el ejecutable `bin-ins.exe` a **Ghidra** para analizar su código.

El análisis de la función `entry` reveló un comportamiento típico de *malware*:
1. **Junk Code:** Código inútil diseñado para engañar a los antivirus y entorpecer el análisis estático.
2. **Navegación del PEB:** Uso de punteros para navegar manualmente las estructuras internas de Windows (`ProcessEnvironmentBlock`) y localizar las secciones del propio ejecutable en memoria.
3. **El Error Intencional:** El programa busca una sección específica calculando un hash (`0x9f520b2d`). Al encontrarla, intenta descifrarla y ejecutarla. Sin embargo, debido a un error de programación introducido por el autor del reto, se pasan punteros nulos a la función encargada de ejecutar el código desempaquetado (el Reflective PE Loader), provocando que el programa termine sin mostrar la bandera.

*[INSERTAR IMAGEN AQUÍ: Captura del descompilador de Ghidra mostrando la función entry, el bucle do-while y la llamada nula (las variables locales inicializadas en 0)]*

### 3. Extracción y Desempaquetado (Unpacking)
Dado que el programa no es capaz de ejecutar su propio payload debido al error lógico, se procedió a extraer la sección secreta manualmente. 

Se desarrolló un script en Python utilizando la librería `pefile` para dumpear todas las secciones del ejecutable a archivos binarios independientes.

Al analizar las secciones extraídas con `binwalk`, se descubrió que la sección ofuscada (`seccion_.ATOM.bin`) contenía datos comprimidos con **LZMA**:

*[INSERTAR IMAGEN AQUÍ: Captura de la terminal ejecutando el comando binwalk y revelando la firma LZMA en la sección .ATOM]*

Se descomprimió el archivo utilizando herramientas nativas de Linux:
```bash
lzma -d < seccion_.ATOM.bin > flag_generator.exe
4. Análisis del Payload Final
El archivo resultante (flag_generator.exe) es un binario PE64 legítimo. Al analizarlo en Ghidra, se descubrió la lógica real para la generación de la bandera.

La función main del nuevo programa también contiene un error lógico intencional: verifica si un descriptor de archivo (handle) devuelto por el sistema operativo es exactamente igual a 0xa. Como esto es altamente improbable, la ejecución normal falla y emite el mensaje [!] I didn't work!.

En lugar de parchear las instrucciones de ensamblador para evadir el salto condicional, se analizó la memoria estática del programa. En la función __static_initialization_and_destruction_0, se encontró que la bandera estaba fragmentada y ofuscada utilizando Base64.

[INSERTAR IMAGEN AQUÍ: Captura de Ghidra mostrando las inicializaciones de las variables DAT_ con las cadenas en Base64]

5. Resultado y Ensamblaje
Los fragmentos extraídos de la memoria del programa fueron:

cGljb0NURns0

MTFfNHIzXzRw

MTVfbjA3aDFu

OV8zbDUzXzRm

NzA2NDBlfQo=

Utilizando la terminal de Linux, se decodificó secuencialmente cada fragmento:

Bash
echo "fragmento" | base64 -d
Flag Obtenida: picoCTF{411_4r3_4p15_n07h1n9_3l53_4f70640e}