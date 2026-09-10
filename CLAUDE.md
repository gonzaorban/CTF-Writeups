# CTF-Writeups — Contexto del proyecto

## Qué es este repo

Writeups de CTF organizados por plataforma y, dentro de cada una, por categoría de vulnerabilidad. Cada desafío vive en su propia carpeta con un `README.md` y una carpeta `images/`.

Plataformas: **HackLab/** (SoftwareSeguro), **picoCTF/**, **tryhackme/** y **google-CTF/**.

Los writeups de HackLab fueron extraídos originalmente desde un PDF con PyMuPDF, por lo que el texto llegó en plano y luego se formateó a mano.

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

Los índices de cada plataforma y categoría (`README.md` de nivel superior) enlazan a cada desafío. El README raíz solo enlaza a las plataformas: el detalle de categorías y desafíos vive en el índice de cada plataforma, no en la raíz.

Si se renombra o agrega una carpeta de desafío, actualizar el índice correspondiente en el mismo commit.

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

## Convención de commits

`fix(plataforma/categoria/nombre-desafio): descripción breve`

---

## Estructura del repo

```
CTF-Writeups/
├── HackLab/                       ← SoftwareSeguro
│   ├── README.md                  ← índice de plataforma
│   ├── introduccion/
│   │   ├── README.md              ← índice de categoría
│   │   └── desafio-1-uso-del-inspector/
│   │       ├── README.md          ← writeup del desafío
│   │       └── images/
│   ├── idor/  xss/  sql-injection/  criptoanalisis/  ...
├── picoCTF/
│   ├── README.md                  ← índice de plataforma
│   ├── 2019/Web/
│   └── 2026/<Categoría>/<Desafío>/
├── tryhackme/                     ← Web/ · Network/
├── google-CTF/                    ← <año>/<Categoría>/<Desafío>/
└── CLAUDE.md                      ← este archivo
```
