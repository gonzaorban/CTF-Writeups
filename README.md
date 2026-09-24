# 🔐 Cybersecurity & CTF Writeups

Este repositorio documenta mis soluciones (writeups), metodologías y scripts desarrollados para resolver desafíos de seguridad informática en distintas plataformas CTF. Cada carpeta corresponde a una plataforma y organiza los desafíos por categoría de vulnerabilidad, con pasos detallados, capturas de pantalla y código de explotación.

---

## 📂 Estructura del repositorio

Cada plataforma tiene su propio índice con el detalle de categorías y desafíos.

| Plataforma | Enlace | Página |
| :--- | :--- | :--- |
| 🏴 **SoftwareSeguro — HackLab** | [HackLab/](./HackLab/) | [softwareseguro.com.ar](https://www.softwareseguro.com.ar/) |
| 🟡 **picoCTF** (2019 · 2026) | [picoCTF/](./picoCTF/) | [picoctf.org](https://picoctf.org/) |
| 🟥 **TryHackMe** | [tryhackme/](./tryhackme/) | [tryhackme.com](https://tryhackme.com/) |
| 🔵 **Google CTF** (2025) | [google-CTF/](./google-CTF/) | [g.co/ctf](https://g.co/ctf) |

---

## 🛡️ Topics Covered

El contenido abarca diversas ramas de la ciberseguridad, enfocándose en la comprensión profunda de las vulnerabilidades y su mitigación.

* **Web Security:** Race Conditions (Turbo Intruder), CSP Bypass, IDOR, XSS to CSRF, JWT Forgery, Mass Assignment, IP Spoofing, LFI, RCE vía CVE.
* **Access Control & Lógica de negocio:** Broken Access Control, Information Disclosure, manipulación de flujos de compra y validaciones del lado del servidor.
* **Autenticación & Tokens:** bypass de login, manejo inseguro de tokens, Local Storage y cookies.
* **SQL Injection:** Blind SQLi, Authentication Bypass, **Exif Metadata Injection**, sqlmap, fallos de sanitización.
* **Cryptography:** RSA Attacks (Common Factor, Franklin-Reiter / Related Messages), LFSR / Shift Registers, Custom Ciphers (Statistical Analysis), Known-Plaintext Attack, Offline Hash Cracking (Salted).
* **Reverse Engineering:** Análisis estático con IDA y Ghidra, instrumentación dinámica con Frida, cracking de binarios y bypass de comprobaciones.
* **Binary Exploitation:** Explotación de binarios con pwntools y GDB, desbordamiento de memoria y manipulación del stack.
* **Blockchain:** Smart contracts en Solidity / web3 (Reentrancy, Access Control).
* **Forensics & Coding:** Image Recovery (Parity Logic), Steganography, Binary Analysis, DNS Enumeration.

---

## 💻 Languages & Tools

![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![SQL](https://img.shields.io/badge/SQL-4479A1?style=for-the-badge&logo=postgresql&logoColor=white)
![Burp Suite](https://img.shields.io/badge/Burp_Suite-FF6633?style=for-the-badge&logo=burpsuite&logoColor=white)
![Java](https://img.shields.io/badge/Java-ED8B00?style=for-the-badge&logo=java&logoColor=white)
![ExifTool](https://img.shields.io/badge/ExifTool-Metadata-green?style=for-the-badge)
![Turbo Intruder](https://img.shields.io/badge/Turbo_Intruder-Concurrency-red?style=for-the-badge)
![IDA](https://img.shields.io/badge/IDA-Disassembler-blue?style=for-the-badge)
![Ghidra](https://img.shields.io/badge/Ghidra-Reversing-red?style=for-the-badge)
![Frida](https://img.shields.io/badge/Frida-Instrumentation-orange?style=for-the-badge)
![Solidity](https://img.shields.io/badge/Solidity-Smart_Contracts-363636?style=for-the-badge&logo=solidity&logoColor=white)

**Librerías clave:** `pwntools`, `requests`, `hashlib`, `aiohttp` (para fuerza bruta asíncrona), `web3`.

---

## ⚡ Featured Techniques

Desglose técnico de vectores de ataque avanzados extraídos de los desafíos más complejos del repositorio.

<details>
<summary><strong>🏎️ Concurrency: Race Condition con Turbo Intruder (Scripting)</strong></summary>
<br>
Explotación de una condición de carrera en lógica de negocios ("El analista") donde se requería asociar ventas a vendedores.
<ul>
  <li><strong>Herramienta:</strong> Turbo Intruder (Extensión de Burp).</li>
  <li><strong>Técnica:</strong> Desarrollo de un script en Python (<code>queueRequests</code>) utilizando el motor <code>RequestEngine</code> para enviar ráfagas de peticiones concurrentes (Cluster Bomb) y superar las validaciones de estado del servidor.</li>
</ul>
</details>

<details>
<summary><strong>🛡️ Web: XSS + CSRF Chaining & CSP Bypass</strong></summary>
<br>
Bypass de Políticas de Seguridad de Contenido (CSP) mal configuradas en el "Blog de HackLab", escalando Stored XSS a CSRF para forzar acciones en nombre de la víctima.
<ul>
  <li><strong>V1 (bypass vía nonce):</strong> extracción de un <code>nonce</code> válido del código fuente para inyectar un bloque <code>&lt;script&gt;</code> autorizado. El XSS se escala a CSRF con jQuery (<code>$.post</code>) para publicar comentarios en nombre de la víctima.</li>
  <li><strong>V2 (bypass vía <code>script-src *</code>):</strong> la CSP bloquea todo script inline pero el comodín <code>*</code> autoriza <code>&lt;script src&gt;</code> remoto (alojado en jsDelivr para pasar ORB). El ataque encadena <strong>dos etapas</strong> según dónde entra cada víctima: la etapa 1 corre en <code>/comments</code> y, vía <code>POST /profile</code> sin CSRF, envenena la bio de un usuario experto; esa bio se muestra en <code>/biographies</code>, la única sección que visita la segunda víctima, cuya carga dispara la etapa 2 (<code>POST /comment</code> con su sesión).</li>
</ul>
</details>

<details>
<summary><strong>📸 SQLi: Inyección vía Metadatos de Imagen (Exif)</strong></summary>
<br>
Inyección SQL atípica en el procesamiento de archivos subidos.
<ul>
  <li><strong>Vector:</strong> El backend (SQLite) leía el metadato EXIF <code>Make</code> sin sanitizar.</li>
  <li><strong>Payload:</strong> Uso de <strong>ExifTool</strong> para inyectar sentencias SQL en la etiqueta <code>Make</code> de una imagen JPG.
  <br><code>exiftool -Make="'|| (SELECT user_id FROM images LIMIT 1)||" test.jpg</code></li>
</ul>
</details>

<details>
<summary><strong>🔐 Crypto: RSA Common Factor & Custom Algo Analysis</strong></summary>
<br>
<ul>
  <li><strong>RSA:</strong> Recuperación de claves privadas mediante el ataque de factor común (GCD) cuando dos módulos $N_1$ y $N_2$ comparten un número primo $q$.</li>
  <li><strong>Custom Cipher:</strong> Criptoanálisis de un algoritmo personalizado (César + Ruido aleatorio). Solución mediante análisis estadístico de frecuencia de palabras y eliminación de ruido basada en la longitud de la clave.</li>
</ul>
</details>

<details>
<summary><strong>🌐 Web: IP Spoofing & JWT Forgery</strong></summary>
<br>
<ul>
  <li><strong>IP Spoofing:</strong> Evasión de restricciones de votación por IP mediante la inyección del header <code>X-Forwarded-For</code> iterando sobre un rango de IPs falsas.</li>
  <li><strong>JWT:</strong> Filtración de una <code>SECRET KEY</code> expuesta en un endpoint JSONP para forjar tokens de administrador válidos (<code>HS256</code>).</li>
</ul>
</details>

---

## 📬 Contacto y correcciones

Si encontrás alguna **incoherencia, error técnico, enlace roto o explicación confusa** en cualquiera de los writeups, escribime — se agradece muchísimo:

* 📧 **Correo:** [gonzaorban@gmail.com](mailto:gonzaorban@gmail.com)
* 🐙 **GitHub:** abrí un [issue](https://github.com/gonzaorban/CTF-Writeups/issues) o un Pull Request con la corrección

También son bienvenidas sugerencias de enfoques alternativos: muchas veces hay más de un camino para resolver el mismo desafío.

---

<p align="center">
  <sub>Desarrollado con fines educativos y de investigación ética.</sub>
</p>
