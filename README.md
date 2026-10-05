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
| 🟠 **PortSwigger — Web Security Academy** | [PortSwigger/](./PortSwigger/) | [portswigger.net](https://portswigger.net/web-security/all-labs) |

Cada desafío vive en su propia carpeta, con un `README.md` (el writeup) y una carpeta `assets/`. Dentro de cada carpeta de desafío:

- **`assets/`** contiene únicamente las **imágenes** del writeup (capturas) y los **archivos que son insumo del desafío** (binarios, `.pcap`, código cliente obtenido del inspector, etc.).
- Los **scripts, solvers y exploits propios** van en la **raíz de la carpeta del desafío**, no en `assets/`.
- *Excepción:* los payloads que se sirven por una URL pública ya publicada (p. ej. scripts XSS cargados vía jsDelivr) se mantienen en `assets/` para no romper esas rutas.

---

## 🛡️ Topics Covered

El contenido abarca diversas ramas de la ciberseguridad, enfocándose en la comprensión profunda de las vulnerabilidades y su mitigación.

* **Web Security:** Race Conditions (Turbo Intruder), CSP Bypass, IDOR, XSS to CSRF, JWT Forgery, Mass Assignment, IP Spoofing, LFI, RCE vía CVE.
* **Access Control & Lógica de negocio:** Broken Access Control, Information Disclosure, manipulación de flujos de compra y validaciones del lado del servidor.
* **Autenticación & Tokens:** bypass de login, manejo inseguro de tokens, Local Storage y cookies.
* **SQL Injection:** Blind SQLi, Authentication Bypass, **Exif Metadata Injection**, **Second-Order SQLi vía User-Agent**, extracción manual con concatenación (`||` en SQLite), sqlmap, fallos de sanitización.
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
<summary><strong>🛡️ Web: XSS + CSRF Chaining & CSP Bypass</strong></summary>
<br>
Bypass de Políticas de Seguridad de Contenido (CSP) mal configuradas en el "Blog de HackLab", escalando Stored XSS a CSRF para forzar acciones en nombre de la víctima.
<ul>
  <li><strong>V1 (bypass vía nonce):</strong> extracción de un <code>nonce</code> válido del código fuente para inyectar un bloque <code>&lt;script&gt;</code> autorizado. El XSS se escala a CSRF con jQuery (<code>$.post</code>) para publicar comentarios en nombre de la víctima.</li>
  <li><strong>V2 (bypass vía <code>script-src *</code>):</strong> la CSP bloquea todo script inline pero el comodín <code>*</code> autoriza <code>&lt;script src&gt;</code> remoto (alojado en jsDelivr para pasar ORB). El ataque encadena <strong>dos etapas</strong> según dónde entra cada víctima: la etapa 1 corre en <code>/comments</code> y, vía <code>POST /profile</code> sin CSRF, envenena la bio de un usuario experto; esa bio se muestra en <code>/biographies</code>, la única sección que visita la segunda víctima, cuya carga dispara la etapa 2 (<code>POST /comment</code> con su sesión).</li>
</ul>
<strong>→ ver writeup:</strong> <a href="./HackLab/xss/desafio-29-blog-hacklab-2024/">V1 (Blog 2024)</a> · <a href="./HackLab/xss/desafio-43-blog-hacklab-v2-hacklab-2025/">V2 (Blog v2 2025)</a>
</details>

<details>
<summary><strong>🌐 Web: IP Spoofing & JWT Forgery</strong></summary>
<br>
<ul>
  <li><strong>IP Spoofing:</strong> Evasión de restricciones de votación por IP mediante la inyección del header <code>X-Forwarded-For</code> iterando sobre un rango de IPs falsas.</li>
  <li><strong>JWT:</strong> Filtración de una <code>SECRET KEY</code> expuesta en un endpoint JSONP para forjar tokens de administrador válidos (<code>HS256</code>).</li>
</ul>
<strong>→ ver writeup:</strong> <a href="./HackLab/broken-access-control/desafio-18-votacion-nueva-version-hacklab-2023/">IP Spoofing (Votación)</a> · <a href="./HackLab/tokens/desafio-15-consulta-de-multas/">JWT (Consulta de multas)</a>
</details>

<details>
<summary><strong>🎭 Web: XS-Leak de dimensiones de imagen cross-origin (CSRF)</strong></summary>
<br>
Fuga de información entre orígenes ("Imagen Importante"), donde el nivel de privilegio de la víctima equivalía a <code>ancho × alto</code> de su foto de perfil, servida en <code>/profile-pic</code> sin identificador —la respuesta dependía solo de la cookie de sesión.
<ul>
  <li><strong>Falla:</strong> <code>/profile-pic</code> con <code>Vary: Cookie</code> y cookie <code>SameSite=None</code>, sin token anti-CSRF ni <code>Cross-Origin-Resource-Policy</code>, de modo que la imagen de la víctima se podía embeber desde otro origen con sus credenciales.</li>
  <li><strong>Técnica:</strong> aunque la Same-Origin Policy impide <strong>leer los bytes</strong> de la imagen cross-origin, <code>naturalWidth</code> y <code>naturalHeight</code> de un <code>&lt;img&gt;</code> sí quedan disponibles. Como el nivel es <code>ancho × alto</code>, medir las dimensiones equivale a filtrar el nivel. Clave: <strong>no</strong> usar <code>crossOrigin = "anonymous"</code>, para que la subrequest viaje con la cookie de la víctima.</li>
  <li><strong>Entrega:</strong> página HTML alojada en un origen público HTTPS (GitHub Pages) que la víctima abre; al <code>onload</code> se leen las dimensiones y se exfiltran a un colector (webhook.site).</li>
</ul>
<strong>→ ver writeup:</strong> <a href="./HackLab/csrf/desafio-40-imagen-importante/">Imagen Importante (HackLab 2025)</a>
</details>

<details>
<summary><strong>🏎️ Concurrency: Race Condition con Turbo Intruder (Scripting)</strong></summary>
<br>
Explotación de una condición de carrera en lógica de negocios ("El analista") donde se requería asociar ventas a vendedores.
<ul>
  <li><strong>Herramienta:</strong> Turbo Intruder (Extensión de Burp).</li>
  <li><strong>Técnica:</strong> Desarrollo de un script en Python (<code>queueRequests</code>) utilizando el motor <code>RequestEngine</code> para enviar ráfagas de peticiones concurrentes (Cluster Bomb) y superar las validaciones de estado del servidor.</li>
</ul>
<strong>→ ver writeup:</strong> <a href="./HackLab/condiciones-de-carrera/desafio-32-el-analista-hacklab-2024/">El analista (HackLab 2024)</a>
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
<strong>→ ver writeup:</strong> <a href="./HackLab/sql-injection/desafio-20-galeria-de-imagenes-hacklab-2023/">Galería de imágenes (HackLab 2023)</a>
</details>

<details>
<summary><strong>🕵️ SQLi: Second-Order vía User-Agent (SQLite)</strong></summary>
<br>
Inyección SQL de segundo orden en una sección de logs ("Logs") que registra el dispositivo de cada visita.
<ul>
  <li><strong>Vector:</strong> El backend (SQLite) guardaba la cabecera HTTP <code>User-Agent</code> en un <code>INSERT</code> sin sanitizar. La inyección se produce al registrar la visita y el resultado se ve luego, al renderizarse la tabla de <code>/logs</code>.</li>
  <li><strong>Descartes:</strong> El HTML se escapaba (sin XSS) y no existía panel <code>/admin</code>; la pista del "administrador" era una tabla <code>users</code> en la base.</li>
  <li><strong>Payload:</strong> Envío del User-Agent con <code>curl -A</code> y extracción manual por concatenación con <code>||</code>, leyendo <code>sqlite_master</code> para enumerar tablas y esquema, y volcando las credenciales del admin.
  <br><code>curl -A "x' || (SELECT group_concat(username || ':' || password) FROM users) || 'x" https://.../</code></li>
</ul>
<strong>→ ver writeup:</strong> <a href="./HackLab/sql-injection/desafio-21-logs-hacklab-2023/">Logs (HackLab 2023)</a>
</details>

<details>
<summary><strong>🔐 Crypto: RSA Common Factor & Custom Algo Analysis</strong></summary>
<br>
<ul>
  <li><strong>RSA:</strong> Recuperación de claves privadas mediante el ataque de factor común (GCD) cuando dos módulos $N_1$ y $N_2$ comparten un número primo $q$.</li>
  <li><strong>Custom Cipher:</strong> Criptoanálisis de un algoritmo personalizado (César + Ruido aleatorio). Solución mediante análisis estadístico de frecuencia de palabras y eliminación de ruido basada en la longitud de la clave.</li>
</ul>
<strong>→ ver writeup:</strong> <a href="./HackLab/criptoanalisis/desafio-30-rsa-robusto-hacklab-2024/">RSA Robusto (HackLab 2024)</a> · <a href="./HackLab/criptoanalisis/desafio-9-algoritmo-personalizado-hacklab-2023/">Algoritmo personalizado (HackLab 2023)</a>
</details>

<details>
<summary><strong>📡 Crypto + WebRTC: Descifrado de sala y abuso de canal P2P (Direct Chat)</strong></summary>
<br>
Chat 1 a 1 ("Direct Chat") donde el bot <code>sniper</code> entrega la clave si recibe dos "zumbidos" con menos de 1 segundo de intervalo (&lt; 1000 ms), pero solo opera en una sala secreta cuyo nombre venía cifrado.
<ul>
  <li><strong>Fase 1 — Crypto:</strong> el nombre de la sala llegaba en Base64, cifrado con <strong>AES-256-CBC</strong> y clave derivada por <strong>PBKDF2-HMAC-SHA256</strong> (contraseña <code>"PIZZA"</code>, 1000 iteraciones, 48 bytes → 32 de clave + 16 de IV). Descifrarlo da el nombre real de la sala a la que se une el bot.</li>
  <li><strong>Fase 2 — WebRTC:</strong> establecido el canal P2P, el cooldown del "zumbido" se valida <strong>del lado del cliente</strong>, así que se envían dos zumbidos consecutivos por el <code>DataChannel</code> dentro de la ventana de 1 s y el bot libera la clave.</li>
</ul>
<strong>→ ver writeup:</strong> <a href="./HackLab/webrtc/desafio-42-direct-chat/">Direct Chat (HackLab 2025)</a>
</details>

<details>
<summary><strong>🎮 Reversing + Lógica: El cliente no es la fuente de verdad (Tetris)</strong></summary>
<br>
Juego de escritorio ("Tetris") cuyo <code>client.pyc</code> (Python 3.10) se desensambla para reconstruir el protocolo de red.
<ul>
  <li><strong>Reversing:</strong> del bytecode surgen el <code>SERVER_DOMAIN</code>/<code>SERVER_PORT</code>, el nombre en 30 bytes fijos y que el puntaje se envía <strong>byte a byte</strong> (<code>send_score</code> encola valores 0–100).</li>
  <li><strong>Lógica:</strong> el puntaje que vale es el que acumula el <strong>servidor</strong> con los bytes recibidos, no el que dibuja el cliente. Reimplementando el cliente (o editando el score en memoria) se envía directamente el puntaje necesario hasta recibir el mensaje <code>GANASTE</code> con la flag.</li>
</ul>
<strong>→ ver writeup:</strong> <a href="./HackLab/reversing-desktop-apps/desafio-45-tetris-hacklab-2025/">Tetris (HackLab 2025)</a>
</details>

<details>
<summary><strong>⛓️ Blockchain: Reentrancy en <code>withdraw()</code> (Reentrance / VulnBank)</strong></summary>
<br>
Auditoría de un smart contract en Solidity ("VulnBank") con una vulnerabilidad clásica de <strong>Reentrancy</strong>.
<ul>
  <li><strong>Vector:</strong> <code>withdraw()</code> envía el Ether con <code>msg.sender.call{value: amount}("")</code> <strong>antes</strong> de actualizar el saldo (violación del patrón checks-effects-interactions).</li>
  <li><strong>Explotación:</strong> como el envío a un contrato dispara su <code>receive()</code>/<code>fallback()</code>, el atacante vuelve a invocar <code>withdraw()</code> de forma recursiva mientras el saldo sigue sin descontarse, drenando los fondos del banco.</li>
</ul>
<strong>→ ver writeup:</strong> <a href="./picoCTF/Blockchain/Reentrance/">Reentrance (picoCTF)</a>
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
