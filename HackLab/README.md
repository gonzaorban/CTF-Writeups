# Desafíos Software Seguro

Writeups de [HackLab (SoftwareSeguro)](https://www.softwareseguro.com.ar/), organizados por categoría de vulnerabilidad.

HackLab es a la vez una plataforma con desafíos permanentes y una **competencia anual**. Los desafíos que pertenecen a una edición de la competencia están listados en la [tabla de ediciones](#desafíos-por-edición-de-la-competencia) al final de este documento, y lo indican en el campo `Edición` de su encabezado.

## Índice de categorías

### [Introducción](./introduccion/)

- [Desafío 1 - Uso del inspector](./introduccion/desafio-1-uso-del-inspector/)
- [Desafío 37 - Local Storage and Cookie](./introduccion/desafio-37-local-storage-and-cookie/)

### [IDOR](./idor/)

- [Desafío 4 - Aldeas inseguras](./idor/desafio-4-aldeas-inseguras/)
- [Desafío 5 - Apagar la IA (HackLab 2023)](./idor/desafio-5-apagar-la-ia-hacklab-2023/)
- [Desafío 22 - Turnero (HackLab 2024)](./idor/desafio-22-turnero-hacklab-2024/)
- [Desafío 23 - Calculadora (HackLab 2024)](./idor/desafio-23-calculadora-hacklab-2024/)
- [Desafío 35 - Aldeas Inseguras V2](./idor/desafio-35-aldeas-inseguras-v2/)
- [Desafío 36 - Notas Universitarias](./idor/desafio-36-notas-universitarias/)
- [Desafío 41 - Reservas de hotel (HackLab 2025)](./idor/desafio-41-reservas-hotel-hacklab-2025/)
- [Desafío 52 - Soporte confidencial (HackingDay 2026)](./idor/desafio-52-soporte-confidencial-hackingday-2026/) — *también en: [Reversing Apk](./reversing-apk/)*
- [Desafío 65 - El Estanque de Pepe (HackLab 2026)](./idor/desafio-65-el-estanque-de-pepe-hacklab-2026/)
- [Desafío NN - Encuentro Obligado (HackLab 2026)](./idor/desafio-NN-encuentro-obligado-hacklab-2026/) — *también en: [Lógica de negocio](./logica-de-negocio/)*

### [Tokens](./tokens/)

- [Desafío 15 - Consulta de multas](./tokens/desafio-15-consulta-de-multas/)
- [Desafío 53 - Hacking HackingDay (HackingDay 2026)](./tokens/desafio-53-hacking-hackingday-hackingday-2026/)

### [XSS](./xss/)

- [Desafío 6 - Búsqueda de usuarios](./xss/desafio-6-busqueda-de-usuarios/)
- [Desafío 7 - El blog de Pepe (HackLab 2023)](./xss/desafio-7-el-blog-de-pepe-hacklab-2023/)
- [Desafío 8 - El blog de Pepe segurizado](./xss/desafio-8-el-blog-de-pepe-segurizado/)
- [Desafío 29 - Blog Hacklab (HackLab 2024)](./xss/desafio-29-blog-hacklab-2024/)
- [Desafío 43 - Blog Hacklab v2 (HackLab 2025)](./xss/desafio-43-blog-hacklab-v2-hacklab-2025/)

### [SQL Injection](./sql-injection/)

- [Desafío 2 - NSA](./sql-injection/desafio-2-nsa/)
- [Desafío 3 - Home Banking](./sql-injection/desafio-3-home-banking/)
- [Desafío 20 - Galería de imágenes (HackLab 2023)](./sql-injection/desafio-20-galeria-de-imagenes-hacklab-2023/)
- [Desafío 21 - Logs (HackLab 2023)](./sql-injection/desafio-21-logs-hacklab-2023/)
- [Desafío 27 - Mis viajes (HackLab 2024)](./sql-injection/desafio-27-mis-viajes-hacklab-2024/)
- [Desafío 44 - Mis Viajes V2 (HackLab 2025)](./sql-injection/desafio-44-mis-viajes-v2/)
- [Desafío 58 - Cuentas Claras (HackLab 2026)](./sql-injection/desafio-58-cuentas-claras-hacklab-2026/)

### [Criptoanálisis](./criptoanalisis/)

- [Desafío 9 - Algoritmo personalizado (HackLab 2023)](./criptoanalisis/desafio-9-algoritmo-personalizado-hacklab-2023/)
- [Desafío 10 - Mensaje cifrado](./criptoanalisis/desafio-10-mensaje-cifrado/)
- [Desafío 13 - Recuperación de imagen (HackLab 2023)](./criptoanalisis/desafio-13-recuperacion-de-imagen-hacklab-2023/)
- [Desafío 25 - Chat Seguro (HackLab 2024)](./criptoanalisis/desafio-25-chat-seguro-hacklab-2024/)
- [Desafío 30 - RSA Robusto (HackLab 2024)](./criptoanalisis/desafio-30-rsa-robusto-hacklab-2024/)
- [Desafío 50 - SatSim](./criptoanalisis/desafio-50-satsim/)
- [Desafío 51 - Imagen Perdida](./criptoanalisis/desafio-51-imagen-perdida/)
- [Desafío 59 - El Casino de Germán (HackLab 2026)](./reversing-desktop-apps/desafio-59-casino-de-german-hacklab-2026/) — *categoría principal: [Reversing Desktop Apps](./reversing-desktop-apps/)*

### [Broken Access Control](./broken-access-control/)

- [Desafío 12 - Votación](./broken-access-control/desafio-12-votacion/)
- [Desafío 17 - Compra de divisas (HackLab 2023)](./broken-access-control/desafio-17-compra-de-divisas-hacklab-2023/)
- [Desafío 18 - Votación nueva versión (HackLab 2023)](./broken-access-control/desafio-18-votacion-nueva-version-hacklab-2023/)
- [Desafío 73 - ArteStudio (HackLab 2026)](./broken-access-control/desafio-73-artestudio-hacklab-2026/)

### [Mass Assignment](./mass-assignment/)

- [Desafío 11 - Gran Rifa 2019](./mass-assignment/desafio-11-gran-rifa-2019/)
- [Desafío 19 - Presupuesto (HackLab 2023)](./mass-assignment/desafio-19-presupuesto-hacklab-2023/)
- [Desafío 24 - Préstamo (HackLab 2024)](./mass-assignment/desafio-24-prestamo-hacklab-2024/)

### [Desbordamiento de memoria](./desbordamiento-de-memoria/)

- [Desafío 14 - Manipulando el Stack](./desbordamiento-de-memoria/desafio-14-manipulando-el-stack/)
- [Desafío 48 - Rompiendo autenticación](./desbordamiento-de-memoria/desafio-48-rompiendo-autenticacion/)

### [Information Disclosure](./information-disclosure/)

- [Desafío 16 - Ventas](./information-disclosure/desafio-16-ventas/)
- [Desafío 26 - Asistencia (HackLab 2024)](./information-disclosure/desafio-26-asistencia-hacklab-2024/)

### [Auth](./auth/)

- [Desafío 33 - ECommerce (HackLab 2024)](./auth/desafio-33-ecommerce-hacklab-2024/)
- [Desafío 34 - Snow Storm (HackLab 2024)](./auth/desafio-34-snow-storm-hacklab-2024/)
- [Desafío 74 - Veltra Bank (HackLab 2026)](./auth/desafio-74-veltra-bank-hacklab-2026/)

### [SSRF](./ssrf/)

- [Desafío 38 - Cotizaciones Dólar](./ssrf/desafio-38-cotizaciones-dolar/)

### [Condiciones de carrera](./condiciones-de-carrera/)

- [Desafío 32 - El analista (HackLab 2024)](./condiciones-de-carrera/desafio-32-el-analista-hacklab-2024/)

### [Lógica de negocio](./logica-de-negocio/)

- [Desafío 47 - Venta de autos (HackLab 2025)](./logica-de-negocio/desafio-47-venta-de-autos-hacklab-2025/)
- [Desafío 67 - ProMarket (HackLab 2026)](./logica-de-negocio/desafio-67-promarket-hacklab-2026/)
- [Desafío NN - Encuentro Obligado (HackLab 2026)](./idor/desafio-NN-encuentro-obligado-hacklab-2026/) — *categoría principal: [IDOR](./idor/)*

### [Sanitización](./sanitizacion/)

- [Desafío 49 - Fix Urgente](./sanitizacion/desafio-49-fix-urgente/)

### [Reversing Desktop Apps](./reversing-desktop-apps/)

- [Desafío 45 - Tetris (HackLab 2025)](./reversing-desktop-apps/desafio-45-tetris-hacklab-2025/)
- [Desafío 59 - El Casino de Germán (HackLab 2026)](./reversing-desktop-apps/desafio-59-casino-de-german-hacklab-2026/)

### [Reversing Apk](./reversing-apk/)

- [Desafío 31 - Libros Gratis (HackLab 2024)](./reversing-apk/desafio-31-libros-gratis-hacklab-2024/)
- [Desafío 46 - Secure Chat (HackLab 2025)](./reversing-apk/desafio-46-secure-chat-hacklab-2025/)
- [Desafío 52 - Soporte confidencial (HackingDay 2026)](./idor/desafio-52-soporte-confidencial-hackingday-2026/) — *categoría principal: [IDOR](./idor/)*
- [Desafío 62 - Capturando al Ladrón (HackLab 2026)](./reversing-apk/desafio-62-capturando-al-ladron-hacklab-2026/)

### [WebRTC](./webrtc/)

- [Desafío 42 - Direct Chat (HackLab 2025)](./webrtc/desafio-42-direct-chat/)

### [CVE](./cve/)

- [Desafío 55 - Cookie envenenada (HackingDay 2026)](./cve/desafio-55-cookie-envenenada-hackingday-2026/)

### [CSRF](./csrf/)

- [Desafío 40 - Imagen Importante (HackLab 2025)](./csrf/desafio-40-imagen-importante/)

### [Fuerza bruta](./fuerza-bruta/)

- [Desafío 39 - El mejor secreto (HackLab 2025)](./fuerza-bruta/desafio-39-el-mejor-secreto-hacklab-2025/)
- [Desafío 46 - Secure Chat (HackLab 2025)](./reversing-apk/desafio-46-secure-chat-hacklab-2025/) — *categoría principal: [Reversing Apk](./reversing-apk/)*

### [RCE](./rce/)

- [Desafío 72 - FabiFiber (HackLab 2026)](./rce/desafio-72-fabifiber-hacklab-2026/)

### [Web LLM](./web-llm/)

- [Desafío 66 - Secreto en el LLM (HackLab 2026)](./web-llm/desafio-66-secreto-en-el-llm-hacklab-2026/)

---

## Desafíos por edición de la competencia

Estos son los desafíos que corresponden a una edición de la competencia anual HackLab. El resto de los desafíos del índice pertenecen al catálogo permanente de la plataforma y no están asociados a una edición.

### HackLab 2026

El puntaje máximo de un desafío en esta edición fue **50**.

| Desafío | Categoría | Puntaje |
| :--- | :--- | :--- |
| [Desafío 58 - Cuentas Claras](./sql-injection/desafio-58-cuentas-claras-hacklab-2026/) | SQL Injection | 30 |
| [Desafío 59 - El Casino de Germán](./reversing-desktop-apps/desafio-59-casino-de-german-hacklab-2026/) | Reversing Desktop Apps - Criptoanálisis | 50 |
| [Desafío 62 - Capturando al Ladrón](./reversing-apk/desafio-62-capturando-al-ladron-hacklab-2026/) | Reversing Apk | 40 |
| [Desafío 65 - El Estanque de Pepe](./idor/desafio-65-el-estanque-de-pepe-hacklab-2026/) | IDOR | 30 |
| [Desafío 66 - Secreto en el LLM](./web-llm/desafio-66-secreto-en-el-llm-hacklab-2026/) | Web LLM | 30 |
| [Desafío 67 - ProMarket](./logica-de-negocio/desafio-67-promarket-hacklab-2026/) | Lógica de negocio | 20 |
| [Desafío 72 - FabiFiber](./rce/desafio-72-fabifiber-hacklab-2026/) | RCE | 30 |
| [Desafío 73 - ArteStudio](./broken-access-control/desafio-73-artestudio-hacklab-2026/) | Broken Access Control | 40 |
| [Desafío 74 - Veltra Bank](./auth/desafio-74-veltra-bank-hacklab-2026/) | Auth | 50 |
| [Encuentro Obligado](./idor/desafio-NN-encuentro-obligado-hacklab-2026/) *(no figura en softwareseguro)* | IDOR - Lógica de negocio *(no confirmada)* | 50 |
| Balrog *(no figura en softwareseguro; sin writeup)* | — | 40 |
| Frandawos Corp *(no figura en softwareseguro; sin writeup)* | — | 30 |

### HackingDay 2026

| Desafío | Categoría |
| :--- | :--- |
| [Desafío 52 - Soporte confidencial](./idor/desafio-52-soporte-confidencial-hackingday-2026/) | IDOR - Reversing Apk |
| [Desafío 53 - Hacking HackingDay](./tokens/desafio-53-hacking-hackingday-hackingday-2026/) | Tokens |
| [Desafío 55 - Cookie envenenada](./cve/desafio-55-cookie-envenenada-hackingday-2026/) | CVE |

### HackLab 2025

El puntaje máximo de un desafío en esta edición fue **45**.

| Desafío | Categoría | Puntaje |
| :--- | :--- | :--- |
| [Desafío 39 - El mejor secreto](./fuerza-bruta/desafio-39-el-mejor-secreto-hacklab-2025/) | Fuerza bruta | 20 |
| [Desafío 40 - Imagen Importante](./csrf/desafio-40-imagen-importante/) | CSRF | 35 |
| [Desafío 41 - Reservas de hotel](./idor/desafio-41-reservas-hotel-hacklab-2025/) | IDOR | 15 |
| [Desafío 42 - Direct Chat](./webrtc/desafio-42-direct-chat/) | WebRTC | 35 |
| [Desafío 43 - Blog Hacklab v2](./xss/desafio-43-blog-hacklab-v2-hacklab-2025/) | XSS | 30 |
| [Desafío 44 - Mis Viajes V2](./sql-injection/desafio-44-mis-viajes-v2/) | SQL Injection | 30 |
| [Desafío 45 - Tetris](./reversing-desktop-apps/desafio-45-tetris-hacklab-2025/) | Reversing Desktop Apps - Lógica de negocio | 30 |
| [Desafío 46 - Secure Chat](./reversing-apk/desafio-46-secure-chat-hacklab-2025/) | Reversing Apk - Fuerza bruta | 25 |
| [Desafío 47 - Venta de autos](./logica-de-negocio/desafio-47-venta-de-autos-hacklab-2025/) | Lógica de negocio | 15 |
| Nova Corp Pro *(no figura en softwareseguro; sin writeup)* | — | 25 |
| Ticket Master Pro *(no figura en softwareseguro; sin writeup)* | — | 25 |
| Vulnerable Wallet *(no figura en softwareseguro; sin writeup)* | — | 45 |

### HackLab 2024

| Desafío | Categoría |
| :--- | :--- |
| [Desafío 22 - Turnero](./idor/desafio-22-turnero-hacklab-2024/) | IDOR |
| [Desafío 23 - Calculadora](./idor/desafio-23-calculadora-hacklab-2024/) | IDOR - Reversing Desktop Apps |
| [Desafío 24 - Préstamo](./mass-assignment/desafio-24-prestamo-hacklab-2024/) | Mass Assignment |
| [Desafío 25 - Chat Seguro](./criptoanalisis/desafio-25-chat-seguro-hacklab-2024/) | Criptoanálisis |
| [Desafío 26 - Asistencia](./information-disclosure/desafio-26-asistencia-hacklab-2024/) | Information Disclosure |
| [Desafío 27 - Mis viajes](./sql-injection/desafio-27-mis-viajes-hacklab-2024/) | SQL Injection |
| [Desafío 29 - Blog Hacklab](./xss/desafio-29-blog-hacklab-2024/) | XSS |
| [Desafío 30 - RSA Robusto](./criptoanalisis/desafio-30-rsa-robusto-hacklab-2024/) | Criptoanálisis |
| [Desafío 31 - Libros Gratis](./reversing-apk/desafio-31-libros-gratis-hacklab-2024/) | Reversing Apk - Broken Access Control |
| [Desafío 32 - El analista](./condiciones-de-carrera/desafio-32-el-analista-hacklab-2024/) | Condiciones de carrera |
| [Desafío 33 - ECommerce](./auth/desafio-33-ecommerce-hacklab-2024/) | Auth |
| [Desafío 34 - Snow Storm](./auth/desafio-34-snow-storm-hacklab-2024/) | Auth |

### HackLab 2023

| Desafío | Categoría |
| :--- | :--- |
| [Desafío 5 - Apagar la IA](./idor/desafio-5-apagar-la-ia-hacklab-2023/) | IDOR |
| [Desafío 7 - El blog de Pepe](./xss/desafio-7-el-blog-de-pepe-hacklab-2023/) | XSS |
| [Desafío 9 - Algoritmo personalizado](./criptoanalisis/desafio-9-algoritmo-personalizado-hacklab-2023/) | Criptoanálisis |
| [Desafío 13 - Recuperación de imagen](./criptoanalisis/desafio-13-recuperacion-de-imagen-hacklab-2023/) | Criptoanálisis |
| [Desafío 17 - Compra de divisas](./broken-access-control/desafio-17-compra-de-divisas-hacklab-2023/) | Broken Access Control |
| [Desafío 18 - Votación nueva versión](./broken-access-control/desafio-18-votacion-nueva-version-hacklab-2023/) | Broken Access Control |
| [Desafío 19 - Presupuesto](./mass-assignment/desafio-19-presupuesto-hacklab-2023/) | Mass Assignment |
| [Desafío 20 - Galería de imágenes](./sql-injection/desafio-20-galeria-de-imagenes-hacklab-2023/) | SQL Injection |
| [Desafío 21 - Logs](./sql-injection/desafio-21-logs-hacklab-2023/) | SQL Injection |
