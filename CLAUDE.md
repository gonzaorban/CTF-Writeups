# CTF-Writeups — Contexto del proyecto

## Qué es este repo

Writeups de CTF organizados por categoría de vulnerabilidad. La carpeta `HackLab/` contiene desafíos extraídos automáticamente desde un PDF con PyMuPDF — el texto llegó en plano, sin formato.

**Tarea activa:** mejorar el formato de cada `README.md` de desafío dentro de `HackLab/`, un desafío a la vez, con commit descriptivo después de cada uno y esperar OK del usuario antes de continuar.

---

## Reglas estrictas

1. NO inventar información, comandos, payloads ni explicaciones que no estén ya escritas
2. NO modificar flags, hashes ni payloads literales (solo envolverlos en code fences)
3. NO renombrar imágenes ni cambiar sus rutas relativas
4. NO tocar los README.md de carpetas raíz o de categoría (solo los de desafíos individuales)

---

## Mejoras a aplicar en cada README de desafío

- **Eliminar** las líneas duplicadas del encabezado (categoría + título repetidos al inicio por el PDF)
- **Envolver en code fences** con lenguaje correcto:
  - Shell → ` ```bash `
  - Python → ` ```python `
  - SQL → ` ```sql `
  - JavaScript → ` ```javascript `
  - HTTP → ` ```http `
  - JSON → ` ```json `
  - Hashes / tokens / sin lenguaje claro → ` ``` ` (sin etiqueta)
- **Reorganizar** imagen/texto solo si es evidentemente incorrecto
- **Agregar `##` headings** (`## Análisis`, `## Explotación`, `## Flag`) solo si el texto original ya separaba esas partes conceptualmente
- **Corregir saltos de línea** raros del PDF (palabras cortadas, oraciones partidas) sin cambiar el significado
- Si algo no se entiende → marcarlo con `<!-- TODO: revisar -->` en lugar de adivinar

---

## Flujo de trabajo por desafío

1. Leer el README.md del desafío
2. Ver imágenes si ayudan al contexto
3. Aplicar mejoras según las reglas
4. Mostrar el diff y hacer `git commit` con mensaje descriptivo:
   `fix(categoria/nombre-desafio): descripción breve`
5. Hacer `git push`
6. Esperar OK del usuario antes de pasar al siguiente

---

## Estado de progreso

### ✅ Completados
- `introduccion/desafio-1-uso-del-inspector/` — formateado, pendiente commit/push

### ⏳ Pendientes (en orden)
2. `introduccion/desafio-37-local-storage-and-cookie/`
3. `idor/desafio-4-aldeas-inseguras/`
4. `idor/desafio-5-apagar-la-ia-hacklab-2023/`
5. `idor/desafio-22-turnero-hackllab-2024/`
6. `idor/desafio-23-calculadora-hackllab-2024/`
7. `idor/desafio-35-aldeas-inseguras-v2/`
8. `idor/desafio-36-notas-universitarias/`
9. `tokens/desafio-15-consultas-multas-falta-hacer/`
10. `xss/desafio-6-busqueda-de-usuarios/`
11. `xss/desafio-7-el-blog-de-pepe-hacklab-2023/`
12. `xss/desafio-8-el-blog-de-pepe-segurizado/`
13. `xss/desafio-29-blog-hacklab-hacklab-2024/`
14. `sql-injection/desafio-2-nsa/`
15. `sql-injection/desafio-3-home-banking/`
16. `sql-injection/desafio-20-galeria-de-imagenes-hacklab-2023/`
17. `sql-injection/desafio-27-mis-viajes/`
18. `criptoanalisis/desafio-9-algoritmo-personalizado-hacklab-2023/`
19. `criptoanalisis/desafio-10-mensaje-cifrado/`
20. `criptoanalisis/desafio-13-recuperacion-de-imagen-hacklab-2023/`
21. `criptoanalisis/desafio-25-chat-seguro-hacklab-2024/`
22. `criptoanalisis/desafio-30-rsa-robusto-hacklab-2024/`
23. `broken-access-control/desafio-12-votacion/`
24. `broken-access-control/desafio-17-compra-de-divisas-hacklab-2023/`
25. `broken-access-control/desafio-18-votacion-nueva-version-hacklab-2023/`
26. `mass-assignment/desafio-11-gran-rifa-2019/`
27. `mass-assignment/desafio-19-presupuesto-hacklab-2023/`
28. `mass-assignment/desafio-23-prestamo-hacklab-2024/`
29. `desbordamiento-de-memoria/desafio-14-manipulando-el-stack/`
30. `information-disclosure/desafio-26-asistencia-hacklab-2024/`
31. `auth/desafio-33-ecommerce-hacklab-2024/`
32. `auth/desafio-34-snow-storm-hacklab-2024/`
33. `condiciones-de-carrera/desafio-32-el-analista-hacklab-2024/`

---

## Estructura del repo

```
CTF-Writeups/
├── HackLab/               ← carpeta con los desafíos a formatear
│   ├── README.md          ← índice raíz (NO tocar)
│   ├── introduccion/
│   │   ├── README.md      ← índice de categoría (NO tocar)
│   │   └── desafio-1-uso-del-inspector/
│   │       ├── README.md  ← estos SÍ se formatean
│   │       └── images/
│   ├── idor/
│   ├── xss/
│   ├── sql-injection/
│   └── ...
├── google-CTF/
├── picoCTF/
├── tryhackme/
└── CLAUDE.md              ← este archivo
```
