# 🔐 Cybersecurity & CTF Writeups

> **Investigación y explotación de vulnerabilidades en entornos controlados.** > *Plataformas: HackTheBox (HTB), SoftwareSeguro.*

Este repositorio documenta mis soluciones (writeups), metodologías y scripts desarrollados para resolver desafíos de seguridad informática y competencias CTF.

---

## 🛡️ Topics Covered

El contenido abarca diversas ramas de la ciberseguridad, enfocándose en la comprensión profunda de las vulnerabilidades y su mitigación.

* **Binary Exploitation (Pwn):** Stack Overflow, Format String, Shellcoding.
* **Web Security:** IDOR, XSS, CSRF, SQL Injection, JWT Attacks, Race Conditions.
* **Cryptography:** RSA Attacks, Hashing collision/cracking.
* **Reverse Engineering:** Análisis estático y dinámico de binarios.

---

## 💻 Languages & Tools

![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![SQL](https://img.shields.io/badge/SQL-4479A1?style=for-the-badge&logo=postgresql&logoColor=white)
![Assembly](https://img.shields.io/badge/Assembly-x64-555555?style=for-the-badge)
![Java](https://img.shields.io/badge/Java-ED8B00?style=for-the-badge&logo=java&logoColor=white)
![Burp Suite](https://img.shields.io/badge/Burp_Suite-FF6633?style=for-the-badge&logo=burpsuite&logoColor=white)
![GDB](https://img.shields.io/badge/GDB-Debugger-CC0000?style=for-the-badge)
![ExifTool](https://img.shields.io/badge/ExifTool-Metadata-green?style=for-the-badge)

**Librerías clave:** `pwntools`, `requests`.

---

## ⚡ Featured Techniques

Desglose técnico de vectores de ataque específicos utilizados en los desafíos. Haz clic para ver los detalles.

<details>
<summary><strong>🕸️ Web: Bypass de is_admin() & RCE en WordPress</strong></summary>
<br>
Análisis de vulnerabilidades lógicas en plugins de WordPress que permiten evadir la verificación de privilegios (<code>is_admin()</code>) y escalar a Ejecución Remota de Código (RCE) mediante la subida de archivos maliciosos.
</details>

<details>
<summary><strong>💥 Pwn: Inyección de Shellcode y manipulación de registros (EBX)</strong></summary>
<br>
Explotación de binarios mediante la inyección de shellcode personalizado en el stack y control del flujo de ejecución sobrescribiendo el registro <code>EIP</code>, asegurando la alineación correcta y manipulando <code>EBX</code> para llamadas al sistema.
</details>

<details>
<summary><strong>💉 SQLi: Inyección basada en booleanos y metadatos (SQLite/ExifTool)</strong></summary>
<br>
Extracción de datos mediante inyecciones SQL ciegas (Boolean-based). Técnica avanzada de inyección de payloads SQL dentro de los metadatos EXIF de una imagen para ser procesados por un backend vulnerable.
</details>

<details>
<summary><strong>🔐 Crypto: Ataque de factor común en RSA & Cracking offline</strong></summary>
<br>
Recuperación de claves privadas RSA utilizando ataques de factor común (cuando el módulo <code>N</code> comparte factores primos). Fuerza bruta offline de PINs utilizando técnicas de salting y rainbow tables.
</details>

<details>
<summary><strong>🏎️ Race Condition: Explotación de concurrencia</strong></summary>
<br>
Uso de <strong>Turbo Intruder</strong> en Burp Suite para enviar múltiples solicitudes simultáneas, explotando ventanas de tiempo críticas en la lógica de negocio (ej. canje de cupones, transferencias).
</details>

---

## 📄 Writeups & Reports

Documentación detallada de competencias recientes.

| Documento | Descripción |
| :--- | :--- |
| **[📄 Ver PDF: HTB University 2025](./path/to/HTB_University_2025.pdf)** | Writeup completo de los desafíos de la competencia universitaria de HackTheBox. |
| **[📄 Ver PDF: SoftwareSeguro - HackLab](./path/to/SoftwareSeguro_HackLab.pdf)** | Informe técnico sobre los laboratorios y máquinas de SoftwareSeguro. |

---

<p align="center">
  <sub>Desarrollado con fines educativos y de investigación ética.</sub>
</p>
