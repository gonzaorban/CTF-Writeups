Piece by Piece
50 points (ordenar dps)

**Plataforma:** picoCTF
**Categoría:** General Skills
**Vulnerabilidad:** Exposición de Secretos en Texto Plano / Manipulación de Flujos Binarios
**Dificultad:** Media
**Herramientas:** Linux Coreutils (`cat`, `file`, `unzip`, `mv`), SSH

### 📂 Estructura de Archivos
* `README.md`: Reporte detallado de la vulnerabilidad y explotación.
* `assets/`: Directorio con las capturas de evidencia.

---

### 1. Reconocimiento
El objetivo requiere acceso inicial vía SSH a una instancia temporal. Al establecer la conexión e inspeccionar el directorio de trabajo del usuario restringido (`ctf-player`), se identifican múltiples archivos fragmentados (`part_aa` a `part_ae`) y un archivo de texto llamado `instructions.txt`. 

![Reconocimiento Inicial](./assets/01-recon.png)

### 2. Análisis de Vulnerabilidad
La lectura del archivo `instructions.txt` revela una falla crítica de seguridad: exposición de credenciales en texto plano (Hardcoded Secrets). El documento detalla que los fragmentos componen un archivo ZIP y expone la contraseña (`supersecret`) necesaria para la extracción. 

Se procede a concatenar los fragmentos aprovechando el *globbing* de la *shell* para respetar el orden alfabético. Al auditar la firma del archivo resultante (Magic Bytes) con la utilidad `file`, se confirma la cabecera `Zip archive data`.

![Evidencia de la Vulnerabilidad](./assets/02-vulnerability.png)

### 3. Explotación
Para interactuar correctamente con la utilidad de extracción, se estandariza el binario asignándole la extensión `.zip`. Posteriormente, se automatiza la descompresión inyectando la credencial obtenida en la fase de reconocimiento directamente como argumento del comando `unzip`, evadiendo el *prompt* interactivo.

**Payload utilizado:**
```bash
# Concatenación de binarios
cat part_* > ensamblado

# Asignación de extensión y descompresión con inyección de password
mv ensamblado ensamblado.zip
unzip -P supersecret ensamblado.zip
```

### 4. Resultado
La extracción es exitosa y genera un archivo `flag.txt` en el directorio actual. Al volcar su contenido, se obtiene la flag que compromete el desafío.

**Flag:** `picoCTF{z1p_and_spl1t_f1l3s_4r3_fun_27804340}`

---

### 🛡️ Remediación (Developer Perspective)
Desde una perspectiva de arquitectura de software y AppSec, este reto simula una mala gestión de artefactos y secretos. Para mitigar estos vectores en un entorno de producción:

* **Gestión Segura de Secretos (Secret Management):** Las contraseñas, tokens o claves de cifrado nunca deben almacenarse en archivos de texto plano dentro del sistema de archivos de la aplicación ni en el control de versiones. Se deben implementar bóvedas de secretos (como HashiCorp Vault, AWS Secrets Manager) o inyectarlos como Variables de Entorno en tiempo de ejecución.
* **Manejo de Archivos Temporales:** Si la aplicación necesita fragmentar o comprimir archivos para procesamiento backend o logística de almacenamiento, estos directorios temporales deben tener permisos estrictos (`chmod 700`) y los artefactos deben ser purgados de memoria e infraestructura inmediatamente después de su uso.