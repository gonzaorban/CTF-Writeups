# 🔐 Cybersecurity & CTF Writeups

Este repositorio documenta mis soluciones (writeups), metodologías y scripts desarrollados para resolver desafíos de seguridad informática en distintas plataformas CTF. Cada carpeta corresponde a una plataforma y organiza los desafíos por categoría de vulnerabilidad, con pasos detallados, capturas de pantalla y código de explotación.

---

## 📂 Estructura del repositorio

```
CTF-Writeups/
├── HackLab/          ← 34 desafíos · SoftwareSeguro · 13 categorías
├── tryhackme/        ←  4 desafíos · Web & Network
├── google-CTF/       ←  1 desafío  · Crypto (2025)
├── picoCTF/          ←  1 desafío  · Web (2019)
└── *.pdf             ← writeups completos en PDF (HTB University, SoftwareSeguro)
```

| Plataforma | Desafío | Categoría |
| :--- | :--- | :--- |
| 🏴 **SoftwareSeguro — HackLab** | [→ Ver todos los desafíos](./HackLab/) | — |
| | [Uso del Inspector](./HackLab/introduccion/desafio-1-uso-del-inspector/) | Introducción |
| | [Local Storage and Cookie](./HackLab/introduccion/desafio-37-local-storage-and-cookie/) | Introducción |
| | [Aldeas Inseguras](./HackLab/idor/desafio-4-aldeas-inseguras/) | IDOR |
| | [Apagar la IA — HackLab 2023](./HackLab/idor/desafio-5-apagar-la-ia-hacklab-2023/) | IDOR |
| | [Turnero — HackLab 2024](./HackLab/idor/desafio-22-turnero-hackllab-2024/) | IDOR |
| | [Calculadora — HackLab 2024](./HackLab/idor/desafio-23-calculadora-hackllab-2024/) | IDOR |
| | [Aldeas Inseguras v2](./HackLab/idor/desafio-35-aldeas-inseguras-v2/) | IDOR |
| | [Notas Universitarias](./HackLab/idor/desafio-36-notas-universitarias/) | IDOR |
| | [Consultas Multas](./HackLab/tokens/desafio-15-consultas-multas-falta-hacer/) | Tokens / JWT |
| | [Búsqueda de Usuarios](./HackLab/xss/desafio-6-busqueda-de-usuarios/) | XSS |
| | [El Blog de Pepe — HackLab 2023](./HackLab/xss/desafio-7-el-blog-de-pepe-hacklab-2023/) | XSS |
| | [El Blog de Pepe Segurizado](./HackLab/xss/desafio-8-el-blog-de-pepe-segurizado/) | XSS |
| | [Blog HackLab 2024](./HackLab/xss/desafio-29-blog-hacklab-hacklab-2024/) | XSS |
| | [NSA](./HackLab/sql-injection/desafio-2-nsa/) | SQL Injection |
| | [Home Banking](./HackLab/sql-injection/desafio-3-home-banking/) | SQL Injection |
| | [Galería de Imágenes — HackLab 2023](./HackLab/sql-injection/desafio-20-galeria-de-imagenes-hacklab-2023/) | SQL Injection |
| | [Mis Viajes](./HackLab/sql-injection/desafio-27-mis-viajes/) | SQL Injection |
| | [Algoritmo Personalizado — HackLab 2023](./HackLab/criptoanalisis/desafio-9-algoritmo-personalizado-hacklab-2023/) | Criptoanálisis |
| | [Mensaje Cifrado](./HackLab/criptoanalisis/desafio-10-mensaje-cifrado/) | Criptoanálisis |
| | [Recuperación de Imagen — HackLab 2023](./HackLab/criptoanalisis/desafio-13-recuperacion-de-imagen-hacklab-2023/) | Criptoanálisis |
| | [Chat Seguro — HackLab 2024](./HackLab/criptoanalisis/desafio-25-chat-seguro-hacklab-2024/) | Criptoanálisis |
| | [RSA Robusto — HackLab 2024](./HackLab/criptoanalisis/desafio-30-rsa-robusto-hacklab-2024/) | Criptoanálisis |
| | [Votación](./HackLab/broken-access-control/desafio-12-votacion/) | Broken Access Control |
| | [Compra de Divisas — HackLab 2023](./HackLab/broken-access-control/desafio-17-compra-de-divisas-hacklab-2023/) | Broken Access Control |
| | [Votación Nueva Versión — HackLab 2023](./HackLab/broken-access-control/desafio-18-votacion-nueva-version-hacklab-2023/) | Broken Access Control |
| | [Gran Rifa 2019](./HackLab/mass-assignment/desafio-11-gran-rifa-2019/) | Mass Assignment |
| | [Presupuesto — HackLab 2023](./HackLab/mass-assignment/desafio-19-presupuesto-hacklab-2023/) | Mass Assignment |
| | [Préstamo — HackLab 2024](./HackLab/mass-assignment/desafio-23-prestamo-hacklab-2024/) | Mass Assignment |
| | [Manipulando el Stack](./HackLab/desbordamiento-de-memoria/desafio-14-manipulando-el-stack/) | Desbordamiento de memoria |
| | [Asistencia — HackLab 2024](./HackLab/information-disclosure/desafio-26-asistencia-hacklab-2024/) | Information Disclosure |
| | [Ecommerce — HackLab 2024](./HackLab/auth/desafio-33-ecommerce-hacklab-2024/) | Auth |
| | [Snow Storm — HackLab 2024](./HackLab/auth/desafio-34-snow-storm-hacklab-2024/) | Auth |
| | [El Analista — HackLab 2024](./HackLab/condiciones-de-carrera/desafio-32-el-analista-hacklab-2024/) | Condiciones de carrera |
| | [Libros Gratis](./HackLab/reversing-apk-broken-access-control/xdesafio-31-libros-gratis/) | Reversing APK |
| 🟥 **TryHackMe** | [→ Ver todos los desafíos](./tryhackme/) | — |
| | [Agent T](./tryhackme/Web/Agent-T/) | Web |
| | [Lo-Fi](./tryhackme/Web/Lo-Fi/) | Web |
| | [Neighbour](./tryhackme/Web/Neighbour/) | Web |
| | [Dig Dug](./tryhackme/Network/Dig-Dug/) | Network |
| 🔵 **Google CTF 2025** | [Numerology](./google-CTF/2025/Crypto/Numerology/) | Crypto |
| 🟡 **picoCTF 2019** | [Irish Name Repo 1](./picoCTF/2019/Web/Irish-Name-Repo-1/) | Web |

---

## 🗂️ HackLab — Categorías

El laboratorio principal de SoftwareSeguro agrupa los desafíos por tipo de vulnerabilidad, cubriendo técnicas reales de ataque web, criptografía y análisis binario.

| Categoría | Desafíos | Enlace |
| :--- | :---: | :--- |
| IDOR | 6 | [idor/](./HackLab/idor/) |
| Criptoanálisis | 5 | [criptoanalisis/](./HackLab/criptoanalisis/) |
| XSS | 4 | [xss/](./HackLab/xss/) |
| SQL Injection | 4 | [sql-injection/](./HackLab/sql-injection/) |
| Broken Access Control | 3 | [broken-access-control/](./HackLab/broken-access-control/) |
| Mass Assignment | 3 | [mass-assignment/](./HackLab/mass-assignment/) |
| Auth | 2 | [auth/](./HackLab/auth/) |
| Introducción | 2 | [introduccion/](./HackLab/introduccion/) |
| Tokens / JWT | 1 | [tokens/](./HackLab/tokens/) |
| Desbordamiento de memoria | 1 | [desbordamiento-de-memoria/](./HackLab/desbordamiento-de-memoria/) |
| Information Disclosure | 1 | [information-disclosure/](./HackLab/information-disclosure/) |
| Condiciones de carrera | 1 | [condiciones-de-carrera/](./HackLab/condiciones-de-carrera/) |
| Reversing APK | 1 | [reversing-apk/](./HackLab/reversing-apk/) |

---

## 🛡️ Topics Covered

El contenido abarca diversas ramas de la ciberseguridad, enfocándose en la comprensión profunda de las vulnerabilidades y su mitigación.

* **Web Security:** Race Conditions (Turbo Intruder), CSP Bypass, IDOR, XSS to CSRF, JWT Forgery, Mass Assignment, IP Spoofing.
* **SQL Injection:** Blind SQLi, Authentication Bypass, **Exif Metadata Injection**.
* **Cryptography:** RSA Attacks (Common Factor), Custom Ciphers (Statistical Analysis), Offline Hash Cracking (Salted).
* **Forensics & Coding:** Image Recovery (Parity Logic), Binary Analysis.

---

## 💻 Languages & Tools

![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![SQL](https://img.shields.io/badge/SQL-4479A1?style=for-the-badge&logo=postgresql&logoColor=white)
![Burp Suite](https://img.shields.io/badge/Burp_Suite-FF6633?style=for-the-badge&logo=burpsuite&logoColor=white)
![Java](https://img.shields.io/badge/Java-ED8B00?style=for-the-badge&logo=java&logoColor=white)
![ExifTool](https://img.shields.io/badge/ExifTool-Metadata-green?style=for-the-badge)
![Turbo Intruder](https://img.shields.io/badge/Turbo_Intruder-Concurrency-red?style=for-the-badge)

**Librerías clave:** `pwntools`, `requests`, `hashlib`, `aiohttp` (para fuerza bruta asíncrona).

---

## ⚡ Featured Techniques

Desglose técnico de vectores de ataque avanzados extraídos de los desafíos más complejos del repositorio.

<details>
<summary><strong>🏎️ Concurrency: Race Condition con Turbo Intruder (Scripting)</strong></summary>
<br>
Explotación de una condición de carrera en lógica de negocios ("El Analista") donde se requería asociar ventas a vendedores.
<ul>
  <li><strong>Herramienta:</strong> Turbo Intruder (Extensión de Burp).</li>
  <li><strong>Técnica:</strong> Desarrollo de un script en Python (<code>queueRequests</code>) utilizando el motor <code>RequestEngine</code> para enviar ráfagas de peticiones concurrentes (Cluster Bomb) y superar las validaciones de estado del servidor.</li>
</ul>
</details>

<details>
<summary><strong>🛡️ Web: XSS + CSRF Chaining & CSP Bypass</strong></summary>
<br>
Bypass de una Política de Seguridad de Contenido (CSP) estricta en "El blog de Pepe".
<ul>
  <li><strong>Técnica:</strong> Extracción de un <code>nonce</code> válido del código fuente para inyectar un bloque <code>&lt;script&gt;</code> autorizado.</li>
  <li><strong>Impacto:</strong> El XSS se escala a un ataque CSRF utilizando jQuery (<code>$.post</code>) para forzar acciones en nombre de la víctima (publicar comentarios no deseados).</li>
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

<p align="center">
  <sub>Desarrollado con fines educativos y de investigación ética.</sub>
</p>
