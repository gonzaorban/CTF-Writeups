# CTF-Writeups — Contexto del proyecto

## Qué es este repo

Writeups de CTF organizados por plataforma y, dentro de cada una, por categoría de vulnerabilidad. Cada desafío vive en su propia carpeta con un `README.md` y una carpeta `images/`.

Plataformas actuales:

- **HackLab/** — 33 desafíos de SoftwareSeguro, 12 categorías. Extraídos originalmente desde un PDF con PyMuPDF y luego formateados a mano. **Esta parte ya está terminada.**
- **picoCTF/** — 28 desafíos: 1 de la edición 2019 (Web) y 27 de la 2026, en 8 categorías.
- **tryhackme/** — 4 desafíos (Web & Network).
- **google-CTF/** — 1 desafío (Crypto, 2025).

---

## Reglas estrictas

1. NO inventar información, comandos, payloads ni explicaciones que no estén ya escritas
2. NO modificar flags, hashes ni payloads literales (solo envolverlos en code fences)
3. NO renombrar imágenes ni cambiar sus rutas relativas
4. NO tocar los README.md de carpetas raíz o de categoría salvo que el usuario lo pida explícitamente (solo se editan los de desafíos individuales)

---

## Convenciones de estructura

Cada plataforma usa su propia nomenclatura; respetarla al crear o mover carpetas:

- **HackLab:** categorías en `kebab-case` español (`sql-injection/`, `broken-access-control/`). Desafíos: `desafio-N-nombre-en-kebab-case/`.
- **picoCTF:** `picoCTF/<año>/<Categoría con espacios>/<Nombre del desafío>/`. Categorías y nombres en inglés, con espacios y mayúsculas tal como aparecen en la plataforma (`Reverse Engineering/`, `Binary Exploitation/`). Al enlazar estas rutas en Markdown, codificar los espacios como `%20`.
- **tryhackme:** `tryhackme/<Área>/<Nombre>/` (`Web/`, `Network/`).
- **google-CTF:** `google-CTF/<año>/<Categoría>/<Nombre>/`.

Los índices raíz y de categoría (`README.md` de nivel superior) enlazan a cada desafío; si se renombra o agrega una carpeta de desafío, actualizar el índice correspondiente en el mismo commit.

---

## Formato de cada README de desafío

- **Eliminar** líneas duplicadas del encabezado (categoría + título repetidos, típico de la extracción del PDF de HackLab)
- **Envolver en code fences** con lenguaje correcto:
  - Shell → ` ```bash `
  - Python → ` ```python `
  - SQL → ` ```sql `
  - JavaScript → ` ```javascript `
  - HTTP → ` ```http `
  - JSON → ` ```json `
  - Solidity → ` ```solidity `
  - Hashes / tokens / sin lenguaje claro → ` ``` ` (sin etiqueta)
- **Agregar `##` headings** (`## Análisis`, `## Explotación`, `## Flag`) solo si el texto original ya separaba esas partes conceptualmente
- **Corregir saltos de línea** raros (palabras cortadas, oraciones partidas) sin cambiar el significado
- Si algo no se entiende → marcarlo con `<!-- TODO: revisar -->` en lugar de adivinar

---

## Flujo de trabajo por desafío

1. Leer el README.md del desafío
2. Ver imágenes si ayudan al contexto
3. Aplicar mejoras según las reglas
4. Mostrar el diff y hacer `git commit` con mensaje descriptivo:
   `fix(plataforma/categoria/nombre-desafio): descripción breve`
5. Hacer `git push`
6. Esperar OK del usuario antes de pasar al siguiente

---

## Estado de progreso

- **HackLab:** completo. Todos los desafíos formateados; no hay pendientes.
- **picoCTF 2026:** desafíos documentados (commit `1c3481b`). Revisar formato si el usuario lo pide.

---

## Estructura del repo

```
CTF-Writeups/
├── HackLab/                       ← 33 desafíos · SoftwareSeguro
│   ├── README.md                  ← índice raíz (no tocar salvo pedido explícito)
│   ├── introduccion/
│   │   ├── README.md              ← índice de categoría (idem)
│   │   └── desafio-1-uso-del-inspector/
│   │       ├── README.md          ← estos SÍ se formatean
│   │       └── images/
│   ├── idor/  xss/  sql-injection/  criptoanalisis/  ...
├── picoCTF/                       ← 28 desafíos
│   ├── 2019/Web/Irish-Name-Repo-1/
│   └── 2026/
│       ├── Reverse Engineering/   ← 9
│       ├── Cryptography/          ← 8
│       ├── Web Exploitation/      ← 4
│       ├── Binary Exploitation/   ← 2
│       ├── Blockchain/            ← 2
│       ├── Forensics/             ← 1
│       └── General Skills/        ← 1
├── tryhackme/                     ← Web/ · Network/
├── google-CTF/2025/Crypto/
└── CLAUDE.md                      ← este archivo
```
