# CTF-Writeups — Contexto del proyecto

## Qué es este repo

Writeups de CTF organizados por plataforma y, dentro de cada una, por categoría de vulnerabilidad. Cada desafío vive en su propia carpeta con un `README.md` y una carpeta `assets/`.

**El año nunca es una carpeta.** La edición a la que pertenece un desafío se declara en el encabezado de su `README.md` y, cuando corresponde, en una tabla de ediciones al final del índice de la plataforma.

Plataformas: **HackLab/** (SoftwareSeguro), **picoCTF/**, **tryhackme/** y **google-CTF/**.

Los writeups de HackLab fueron extraídos originalmente desde un PDF con PyMuPDF, por lo que el texto llegó en plano y luego se formateó a mano.

---

## Reglas estrictas

1. NO inventar información, comandos, payloads ni explicaciones que no estén ya escritas
2. NO modificar flags, hashes ni payloads literales (solo envolverlos en code fences)
3. NO renombrar archivos de imagen ni cambiar sus rutas relativas (la carpeta contenedora es siempre `assets/`)
4. NO tocar los README.md de carpetas raíz o de categoría salvo que el usuario lo pida explícitamente (solo se editan los de desafíos individuales)

---

## Convenciones de estructura

Cada plataforma usa su propia nomenclatura; respetarla al crear o mover carpetas:

Todas las plataformas siguen el mismo esquema de dos niveles: `<plataforma>/<Categoría>/<Nombre del desafío>/`. Cada plataforma usa su propia nomenclatura; respetarla al crear o mover carpetas:

- **HackLab:** categorías en `kebab-case` español (`sql-injection/`, `broken-access-control/`). Desafíos: `desafio-N-nombre-en-kebab-case/`.
- **picoCTF:** `picoCTF/<Categoría con espacios>/<Nombre del desafío>/`. Categorías y nombres en inglés, con espacios y mayúsculas tal como aparecen en la plataforma (`Reverse Engineering/`, `Binary Exploitation/`). Al enlazar estas rutas en Markdown, codificar los espacios como `%20`. Si una categoría cambió de nombre entre ediciones, usar el nombre actual (por eso el desafío de 2019 vive en `Web Exploitation/`, no en `Web/`).
- **tryhackme:** `tryhackme/<Área>/<Nombre>/` (`Web/`, `Network/`).
- **google-CTF:** `google-CTF/<Categoría>/<Nombre>/`.

### Contenido de la carpeta de un desafío

- `assets/` es **solo** para las imágenes del writeup (capturas) y los archivos que son *insumo del desafío* (lo que da la plataforma o se obtiene analizándolo: binarios, `.pcap`, el código cliente encontrado en el inspector, etc.).
- Los **scripts, solvers y exploits propios** (los que uno escribe para resolver el desafío) van en la **raíz de la carpeta del desafío**, no en `assets/`. Se enlazan con ruta relativa a la raíz del desafío (`./solve.py`).
- **Excepción:** un payload que se sirve por URL pública (p. ej. XSS cargados vía jsDelivr con la ruta `.../assets/x.js` embebida en el enunciado o el propio payload) se deja en `assets/`, porque necesita una ruta estable ya publicada; mover esos archivos rompería las URLs.

Los índices de cada plataforma y categoría (`README.md` de nivel superior) enlazan a cada desafío. El README raíz solo enlaza a las plataformas: el detalle de categorías y desafíos vive en el índice de cada plataforma, no en la raíz.

En los índices de plataformas con varias ediciones, indicar el año junto a cada desafío y cerrar con una tabla "Desafíos por edición".

Si se renombra o agrega una carpeta de desafío, actualizar el índice correspondiente en el mismo commit.

**Desafíos con más de una categoría** (ej. `**Categoría:** Reversing Desktop Apps - Lógica de negocio`): la carpeta vive solo en su categoría principal (la carpeta donde ya está; no se duplica ni se mueve), y el índice de cada categoría secundaria también lo lista, en orden por número, con ruta relativa `../` y la aclaración de su categoría principal:

```markdown
- [Desafío 45 - Tetris (HackLab 2025)](../reversing-desktop-apps/desafio-45-tetris-hacklab-2025/) — *categoría principal: [Reversing Desktop Apps](../reversing-desktop-apps/)*
```

Al agregar un desafío con doble categoría, actualizar en el mismo commit los índices de todas sus categorías.

---

## Formato de cada README de desafío

- **Eliminar** líneas duplicadas del encabezado (categoría + título repetidos, típico de la extracción del PDF de HackLab)
- **Bloque de metadata** después del `# título`, con dos espacios al final de cada línea. `Edición` solo si el desafío pertenece a una edición de la competencia:

  ```markdown
  **Plataforma:** HackLab (SoftwareSeguro)
  **Edición:** HackLab 2023
  **Categoría:** Broken Access Control
  ```

  En picoCTF, TryHackMe, Google CTF y PortSwigger el año (o la nomenclatura de la plataforma) va dentro de `Plataforma` (`**Plataforma:** picoCTF 2026`).

  Campos opcionales en cualquier desafío (de cualquier plataforma): `Dificultad` y `Herramientas` (las herramientas usadas en el writeup, ej. `**Herramientas:** Burp Suite (Repeater)`); completarlos solo si están documentados. No usar el campo `Vulnerabilidad`.
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
- **Sección `🛡️ Remediación (Developer Perspective)`**: opcional, según el tipo de desafío. Incluirla **solo cuando exista una contramedida concreta y específica del desafío**:
  - **Sí** en vulnerabilidades de aplicación web (HackLab, PortSwigger, TryHackMe Web, etc.): es parte del valor del writeup.
  - **No** en CTF de crypto, reversing, forense, pwn o stego, salvo que haya una lección defensiva concreta y no obvia.
  - Nunca rellenar por costumbre con texto genérico: si la remediación sería trivial o inventada, omitir la sección (coherente con la regla nº1: no inventar).

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
│   │       └── assets/
│   ├── idor/  xss/  sql-injection/  criptoanalisis/  ...
├── picoCTF/
│   ├── README.md                  ← índice de plataforma
│   ├── Web Exploitation/<Desafío>/
│   └── Cryptography/  Reverse Engineering/  Blockchain/  ...
├── tryhackme/                     ← Web/ · Network/
├── google-CTF/                    ← <Categoría>/<Desafío>/
└── CLAUDE.md                      ← este archivo
```
