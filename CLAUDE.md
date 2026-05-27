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

Todos los desafíos existentes están formateados. No hay pendientes.

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
