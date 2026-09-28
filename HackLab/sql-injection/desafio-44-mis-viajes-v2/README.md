# Desafío 44 - Mis Viajes V2 (HackLab 2025)

**Plataforma:** HackLab (SoftwareSeguro)
**Edición:** HackLab 2025
**Categoría:** SQL Injection

> ⚠️ **Writeup en progreso (WIP).** La vulnerabilidad está confirmada (SQL Injection
> ejecutable a través del texto que el OCR extrae de la imagen), pero la extracción del
> `user_id` de la víctima todavía no se completó por limitaciones de lectura del OCR sobre
> ciertas palabras clave (`FROM images`). Se documenta todo lo probado como caso de prueba.

## Enunciado

Un año atrás, un amigo había creado una plataforma para guardar imágenes de viajes. En el
HackLab 2024 la vulneraron muchas veces (ver [Desafío 27 - Mis viajes](../desafio-27-mis-viajes-hacklab-2024/)).
En la V2 "solucionó todos los problemas" y agregó funcionalidades. El objetivo es
**visualizar una imagen que no te pertenece**, que contiene el código ganador en su interior,
posiblemente **camuflado**.

## Diferencias con la V1 (2024)

La V1 ([Desafío 27](../desafio-27-mis-viajes-hacklab-2024/)) era SQLi vía EXIF `Make`/`Model`
con ExifTool sobre SQLite. La V2 **parchea ese vector** (los campos EXIF se guardan
HTML-escapados) y agrega funcionalidades nuevas: **clasificador de imagen** ("¿es un viaje?"),
**OCR** (resumen del texto de la imagen) y **mapa GPS** (Leaflet).

## Mapa de la aplicación

- **Sin sesión ni login.** La identidad es solo el `user_id` (UUID) que viaja en el body y
  está renderizado en el HTML (`<input id="id_user" ...>`).
- `GET /images/<uuid>` — único endpoint de lectura. Devuelve JSON con las imágenes de ese
  `user_id`. Usa un converter Flask `<uuid>` **estricto**: cualquier cosa que no sea un UUID
  válido da 404 (no inyectable por el path).
- `POST /upload` — recibe JSON `{image: "data:image/...;base64,...", description, user_id}`.
  Corre: clasificador → EXIF/GPS → **OCR** → `INSERT` en tabla `images`.
- `/uploads/<filename>` — sirve la imagen del filesystem por nombre (UUID.jpg). No consulta DB.
- El `id` de imagen es **global y secuencial**. Las propias dejan huecos (ids `1,3,4,5,13,14,15`
  pertenecen a la víctima; probablemente la ganadora es `id=1`).
- **Instancia propia spawneada:** la DB se siembra al lanzar, con datos deterministas (el
  `user_id` propio y el de la víctima son fijos entre instancias).

## Vector confirmado: SQL Injection vía OCR

El texto que el OCR extrae de la imagen se concatena en la consulta `INSERT` sin parametrizar.
El clasificador exige que la imagen "parezca un viaje", así que el payload se **pinta como texto
sobre una foto de paisaje real** que pasa el clasificador.

### Prueba de ejecución

Pintando en la imagen:

```sql
9'||(SELECT sqlite_version())||'9
```

el campo `summary_ocr` se guarda como `93.46.19`, es decir `9` + `3.46.19` (versión de SQLite)
+ `9`. **La subconsulta se ejecutó** → SQLi confirmada. El motor es **SQLite 3.46.1**.

Test de aislamiento (mismo formato de imagen, distinta validez SQL):

| Payload pintado | Resultado |
|---|---|
| `9'||(SELECT sqlite_version())||'9` | `200`, `ocr='93.46.19'` (ejecutó) |
| `9'||(CASE WHEN 1=1 THEN 65 ELSE 66 END)||'9` | `200`, `ocr='9659'` (ejecutó, `65`) |
| `9'||(XXXX WXXX 1=1 ...)||'9` (SQL inválido, misma forma) | `500` |

Que el status dependa de la **validez SQL** (y no solo de la forma del texto) prueba que la
inyección es real, no ruido del pipeline.

### El envoltorio `9'...'9`

El OCR deforma las comillas según su posición:
- Una comilla de **apertura aislada** se lee como `*`.
- El `||` al inicio de línea se lee como `| |` (con espacio), que no es concatenación válida.
- Una comilla **pegada a un dígito** (`9'`) o a `||` se lee bien.

Por eso el payload se envuelve entre dígitos: `9'||( ... )||'9`. El `9` ancla las comillas y
el `||` para que el OCR los reproduzca correctamente.

## Obstáculo actual (sin resolver)

Las subconsultas **sin** `FROM` (como `sqlite_version()` o `CASE WHEN`) se ejecutan bien.
Las que leen la tabla (`SELECT user_id FROM images ...`) devuelven **500**: el OCR reordena o
deforma la secuencia `FROM images` (por ejemplo la lee como `images ... FROM`), rompiendo la
sintaxis. Como **texto plano** el OCR sí lee `SELECT user_id FROM images WHERE id=1` en orden
correcto, pero dentro del envoltorio ejecutable falla.

Enfoques probados para sortearlo (todos 500 hasta ahora):
- Reemplazar espacios por comentarios `/**/`.
- Identificadores con corchetes `FROM[images]` y paréntesis `FROM(images)`.
- Evitar `=`/`count(*)`: `WHERE id IS 1`, `IN(1)`, `LIMIT 1`, `max(id)`.
- Variar tamaño/ancho de la imagen (romper o restaurar el formato que lee bien).

**Próximo paso:** pintar el texto de la consulta que falla como literal plano (sin el
envoltorio que rompe el SQL) para **ver exactamente cómo el OCR reordena** `FROM images`, y
construir una forma que el OCR reproduzca en orden SQL válido. Una vez leído el `user_id` de la
víctima, `GET /images/<uuid-víctima>` da los filenames y la imagen ganadora se baja de
`/uploads/<filename>` para extraer el código camuflado.

## Vectores descartados (con evidencia)

Antes de dar con el OCR se descartaron, con pruebas:

- **EXIF `Make`/`Model`/`DateTimeOriginal`** (ExifTool + error-based + time-based) → HTML-escapados (`&#39;`), no ejecutan.
- **GPS** lat/long (numéricos, ExifTool valida) y campos GPS-string (`MapDatum`, `ProcessingMethod`, etc.) → ignorados; `GPSLatitudeRef` solo se compara con `S` para el signo.
- **`user_id` y `description`** del body → parametrizados.
- **Path** `GET /images/<uuid>` → converter `<uuid>` estricto.
- **Headers HTTP** (`User-Agent`, `X-Forwarded-For`, `Referer`, ...) time-based → sin efecto.
- **`/uploads/<filename>`** → filesystem, sin traversal ni SQL.
- **Endpoints** `/search`, `/api/search`, etc. → 404 genérico (no existen).
- **Segundo orden** (payload guardado que dispara query en el listado) → sin efecto.
- **Mass assignment** (campos extra en el body) → ignorados.
- **`main.js` React** que aparecía en DevTools bajo `/images/<nil>/main.js` → resultó ser de
  una **extensión de Chrome** del navegador, no del reto (pista falsa).

## Scripts

Todos los scripts de la investigación están en [`scripts/`](./scripts/). Los más relevantes del
camino confirmado:

- [`scripts/v2_isolate.py`](./scripts/v2_isolate.py) — prueba de aislamiento que **confirma la
  SQLi vía OCR** (`sqlite_version()` → `93.46.19`).
- [`scripts/v2_dump.py`](./scripts/v2_dump.py) — intento de volcado directo del `user_id` víctima.
- [`scripts/v2_seeocr.py`](./scripts/v2_seeocr.py) — diagnóstico de cómo el OCR reordena `FROM images` (paso actual).
- [`scripts/v2_exact.py`](./scripts/v2_exact.py) — formato de imagen exacto que el OCR lee bien.

> **Nota:** los scripts obtienen el `user_id` propio del HTML en tiempo de ejecución y apuntan a
> la URL de la instancia (cambia en cada spawn — actualizar la constante `BASE`). Requieren
> `pillow`, `piexif` y `requests`, y ExifTool para los scripts `.sh`.

## Flag

```
<!-- TODO: pendiente — completar la lectura de FROM images vía OCR para obtener el user_id víctima -->
```
