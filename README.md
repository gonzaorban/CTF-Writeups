# 🔐 Cybersecurity & CTF Writeups

> **Investigación y explotación de vulnerabilidades en entornos controlados.**
> *Plataformas: TryHackMe, SoftwareSeguro, picoCTF, HackTheBox (HTB).*

Este repositorio documenta mis soluciones (writeups), metodologías y scripts desarrollados para resolver desafíos de seguridad informática y competencias CTF.

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

## 📄 Writeups & Reports

Documentación detallada de competencias y laboratorios.

| Carpeta | Descripción |
| :--- | :--- |
| **[🔐 SoftwareSeguro - HackLab](./HackLab/)** | +30 desafíos resueltos organizados por categoría de vulnerabilidad. Incluye scripts en Python para fuerza bruta, decodificadores Java para recuperación de imágenes, y guías paso a paso de Burp Suite. |
| **[📄 HTB University 2025](./HTB_University_2025.pdf)** | Writeup de los desafíos de la competencia universitaria de HackTheBox. |

---

<p align="center">
  <sub>Desarrollado con fines educativos y de investigación ética.</sub>
</p>
