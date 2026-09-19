# 🎯 Silent Stream

**Plataforma:** picoCTF 2026
**Categoría:** Forensics
**Vulnerabilidad:** Exfiltración de Datos en Texto Claro (Ofuscación Custom) / Cifrado César a nivel de bytes
**Dificultad:** Media
**Herramientas:** Wireshark, Python (`scapy`), `file`

### 📂 Estructura de Archivos
* `README.md`: Reporte detallado del análisis forense de red y descifrado.
* `encrypt.py`: Script de ofuscación utilizado por el atacante.
* `packets.pcap`: Captura de red con la exfiltración.
* `script.py`: Script automatizado para la extracción de paquetes y reconstrucción del archivo.
* `assets/`: Directorio con las capturas de evidencia (incluye la imagen reconstruida `flag.jpg`).

---

### 1. Reconocimiento
Se nos proporcionan dos archivos: un script de Python (`encrypt.py`) utilizado por un atacante y un archivo de captura de red (`packets.pcap`).

![ls -la mostrando encrypt.py y packets.pcap](./assets/CTF_2026-03-12_00-29-23.png)

Al analizar `encrypt.py`, se descubre la lógica utilizada para ofuscar los datos antes de exfiltrarlos. El atacante implementó una función matemática a nivel de bytes:
```python
def encode_byte(b, key):
    return (b + key) % 256
```
El script revela que la llave estática (`key`) utilizada para esta operación es `42`.

![cat encrypt.py mostrando encode_byte y la llave key=42](./assets/CTF_2026-03-12_00-29-30.png)
*El código del atacante suma una llave fija (42) a cada byte antes de transmitirlo.*

### 2. Análisis de Vulnerabilidad
La ofuscación implementada es funcionalmente equivalente a un Cifrado César a nivel de bytes (Byte-wise Shift Cipher). Al ser una operación aritmética de suma simple con módulo 256, es trivialmente reversible restando la llave y aplicando nuevamente el módulo para manejar los desbordamientos negativos (underflow):
```
decrypted_byte = (encoded_byte - 42) % 256
```

Al analizar el archivo `packets.pcap` con Wireshark, se observa un flujo TCP desde la IP del atacante (`10.10.10.10`) hacia el destino (`10.10.10.11`) por el puerto 9000. Los datos cifrados viajan fragmentados en el payload (Raw Data) de estos paquetes.

![Wireshark mostrando el flujo TCP de 10.10.10.10 a 10.10.10.11 puerto 9000 con el payload cifrado](./assets/CTF_2026-03-12_00-36-11.png)
*El tráfico exfiltra los datos ofuscados en el payload (Raw) de paquetes TCP hacia el puerto 9000.*

### 3. Explotación
Se desarrolla un script en Python utilizando la biblioteca `scapy` para automatizar la extracción de la capa de datos (Raw) de los paquetes TCP correspondientes al flujo del atacante, decodificar los bytes en memoria y reconstruir el archivo original.

**Script de Explotación (`script.py`):**
```python
from scapy.all import rdpcap, TCP, Raw

packets = rdpcap('packets.pcap')
raw_data = b''

for pkt in packets:
    if pkt.haslayer(TCP) and pkt.haslayer(Raw):
        if pkt['IP'].src == '10.10.10.10':
            raw_data += pkt[Raw].load

key = 42
decrypted_data = bytearray()
for b in raw_data:
    decrypted_byte = (b - key) % 256
    decrypted_data.append(decrypted_byte)

with open('reconstructed_file', 'wb') as f:
    f.write(decrypted_data)
```

![Ejecución de script.py extrayendo 9137 bytes cifrados y guardando el archivo descifrado](./assets/CTF_2026-03-12_00-40-30.png)
*El script reensambla los payloads, revierte el cifrado y guarda el archivo reconstruido.*

**Análisis Forense Post-Descifrado:**
El archivo reconstruido no es texto plano legible. Aplicando la utilidad `file` (`file reconstructed_file`), se detectan las firmas hexadecimales (magic bytes) de un archivo de imagen JPEG. Se renombra el archivo con la extensión correcta (`.jpg`) para su visualización.

![file sobre el archivo reconstruido mostrando JPEG image data](./assets/CTF_2026-03-12_01-14-44.png)
*Los magic bytes revelan que el archivo reconstruido es una imagen JPEG (800×500).*

![mv del archivo a flag.jpg y xdg-open para visualizarlo](./assets/CTF_2026-03-12_01-17-07.png)

### 4. Resultado
Al abrir la imagen reconstruida, se visualiza la bandera incrustada en el gráfico.

![Imagen JPEG reconstruida con la bandera incrustada](./assets/flag.jpg)
*La imagen exfiltrada contiene la bandera del desafío.*

**Flag:** `picoCTF{tr4ck_th3_tr4ff1c_2e5a2c18}`

---

### 🛡️ Remediación (Blue Team Perspective)
* **Inspección Profunda de Paquetes (DPI):** Las soluciones de red deben estar configuradas para alertar sobre flujos de datos anómalos o payloads no estándar que intentan evadir los controles de seguridad comunes.
* **Prevención de Pérdida de Datos (DLP):** Los mecanismos de exfiltración simples como este pueden ser mitigados bloqueando transferencias hacia IPs y puertos desconocidos o no autorizados dentro de la red.
