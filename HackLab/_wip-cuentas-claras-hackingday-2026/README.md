# Cuentas Claras

**Plataforma:** HackLab (SoftwareSeguro)

**Edición:** HackingDay 2026

**Categoría:** *(sin asignar — desafío sin resolver)*

**Herramientas:** curl, Burp Suite (Turbo Intruder), flask-unsign

> ## ⚠️ ESTADO: NO RESUELTO
>
> Este writeup documenta el **reconocimiento y los vectores descartados** hasta ahora.
> **La flag todavía no se obtuvo.** Sirve como punto de partida para retomar el desafío:
> todo lo que está acá ya fue probado y verificado, para no repetir trabajo.

## Enunciado

Cuentas Claras es una herramienta interna de contaduría.

Hay 20 categorías, pero el selector solo deja elegir 17: hay **3 categorías restringidas**
a las que no se puede dar de alta proveedores (ni aparecen en el selector ni el servidor
las acepta). Esas 3 categorías igual **tienen movimientos cargados**.

**Objetivo:** averiguar cuántos movimientos hay en las 3 categorías restringidas, sumarlos,
y la flag es el **hash MD5 de esa suma**.

## Superficie de la aplicación

App Flask (Werkzeug) detrás de nginx. Server-rendered, **sin JavaScript** en el cliente.
Solo existen **tres endpoints**:

- `GET /` — lista de proveedores (tabla) + formulario de alta.
- `POST /alta` — crea proveedor. Campos: `nombre`, `categoria`. Redirige a `/` con un *flash*.
- `POST /movimientos/<int:id>` — cuenta movimientos **del proveedor con ese id**.
  Redirige a `/`; el resultado viaja en el **flash de la cookie de sesión** (ver abajo).

Nada más responde: `/categorias`, `/api`, `/reportes`, `/admin`, `/proveedor(es)`,
`/static/` (listado), `/.git/`, fuente (`.py`), `.db`, etc. → **todos 404**.
`robots.txt` solo tiene `Disallow: /`.

### El resultado viaja en la cookie de sesión (no en el body)

`POST /movimientos/<id>` siempre responde **302** con body "Redirecting…". El mensaje real
está en el flash de Flask, dentro del header `Set-Cookie: session=...` (base64url, **firmado
pero no cifrado**). Decodificando el primer segmento:

```bash
# token = primer segmento de la cookie 'session' (antes del primer punto)
echo "$token" | tr '_-' '/+' | base64 -d
# -> {"_flashes":[{" t":["ok","Proveedor #1: 2576 movimientos registrados."]}]}
```

Tres respuestas posibles del flash:

```
"ok"    -> "Proveedor #N: X movimientos registrados."   (el proveedor N existe)
"ok"    -> "Proveedor #N: 0 movimientos registrados."   (existe pero sin movimientos)
"error" -> "No se pudo contar los movimientos para ese proveedor."  (N no existe)
```

Esto permite enumerar con **1 request por id** leyendo el `Set-Cookie` (ver
[`turbo_movimientos.py`](./turbo_movimientos.py)).

## Datos del seed (constantes entre instancias)

Al reiniciar, el seed inserta **exactamente 3 proveedores**, con un timestamp de alta
**hardcodeado e idéntico** (es la huella del seed; **no cambia entre instancias**):

| id | nombre              | categoría  | movimientos | fecha de alta                 |
|----|---------------------|------------|-------------|-------------------------------|
| 1  | Libreria Central    | Papeleria  | **2576**    | `2026-10-09 18:47:50.202459`  |
| 2  | Transporte Sur      | Transporte | **3104**    | `2026-10-09 18:47:50.202459`  |
| 3  | Catering del Valle  | Catering   | **1897**    | `2026-10-09 18:47:50.202459`  |

- El microsegundo **`202459`** es constante entre instancias (dato confirmado).
- Las tres categorías del seed (Papeleria, Transporte, Catering) **son permitidas**.
- El próximo proveedor creado toma **id 4** → **no hay proveedores ocultos** intercalados
  en el autoincrement.

### Las 17 categorías del selector (orden alfabético)

```
Capacitacion, Catering, Consultoria, Insumos, Limpieza, Logistica, Mantenimiento,
Marketing, Mobiliario, Papeleria, Seguridad, Servicios, Software, Tecnologia,
Telefonia, Transporte, Viaticos
```

Las **3 restringidas** son las que faltan para llegar a 20. Sus nombres **se desconocen**:
`/alta` responde lo mismo (`"Categoría inválida o restringida…"`) tanto para una categoría
restringida real como para un nombre inexistente, así que ese mensaje **no sirve** para
distinguirlas ni para enumerarlas.

## Vectores probados y DESCARTADOS (con evidencia)

| # | Vector | Prueba realizada | Resultado |
|---|--------|------------------|-----------|
| 1 | Enumerar proveedores por id | Barrido `0–20000` (Turbo Intruder, 20001 reqs, 0 fails) sobre instancia limpia | **Solo ids 1,2,3 tienen movimientos.** Sin proveedores ocultos. |
| 2 | Conteo por **categoría** del proveedor | Crear 1 proveedor en cada una de las 17 categorías y contar | **Todos dan 0.** El conteo NO sigue el string de categoría; va atado al `proveedor_id` sembrado. |
| 3 | SQLi en `/movimientos/<id>` (path) | `3'`, `1a`, etc. | Route es `<int>` estricto → **404**. Imposible inyectar. |
| 4 | SQLi — id por body/query | `proveedor_id=`, `id=`, `?id=` sobre `/movimientos/3` | **Ignorados** (id solo del path). |
| 5 | SQLi en `nombre` (`/alta`) | `nombre','x'),('y` ; `t6' \|\| (SELECT '1')` | Se guardan **literales** → INSERT **parametrizado**. |
| 6 | SQLi en `categoria` (`/alta`) | comilla, `OR 1=1`, `';--`, **time-based** `randomblob(50000000)` | Whitelist corta **antes** de tocar la BD; payloads **no tardan**. Sin inyección. |
| 7 | Bypass whitelist de `categoria` | multi-valor (`categoria=X&categoria=Y`), JSON body, mayúsc., espacios | Toma el 1er valor y hace `.strip()`; inválidas **no insertan**. |
| 8 | Mass assignment en `/alta` | `id=777`, `fecha=2000-01-01` | **Ignorados** (id autoincremental, fecha = now). |
| 9 | Filtros/params en `/` | `?categoria=`, `?cat=`, `?all=1`, `?orden=`, `?desde=` | Sin efecto (misma respuesta, 7712 bytes). |
| 10 | Rutas ocultas / fuente | `/source`, `/.git/`, `*.py`, `*.db`, `/static/` listado, `/admin`, `/reportes`… | **Todos 404.** |
| 11 | Tracebacks / modo debug | GET a endpoint POST, `/alta` sin campos, multipart roto, ids enteros gigantes | Errores manejados con gracia → **sin traceback** (Flask no está en debug). |
| 12 | Cookie de sesión Flask | Decodificada: solo contiene `_flashes`, **ningún campo de rol/usuario** | Forjarla (si el SECRET_KEY fuera débil) no habilitaría nada observado. *(crackeo offline no completado)* |

## Conclusión parcial

- El conteo de `/movimientos/<id>` es **estrictamente por `proveedor_id`**, y solo los 3
  proveedores del seed (ids 1,2,3) tienen movimientos.
- **No hay** proveedores de categorías restringidas enumerables por este endpoint
  (barrido 0–20000 limpio, sin huecos de id).
- La aplicación es **robusta**: queries parametrizadas, whitelist estricta, sin fugas de
  fuente ni tracebacks. **No se encontró un vector técnico clásico (SQLi/IDOR enumerable).**

La contradicción pendiente: el enunciado afirma que las 3 categorías restringidas *tienen
movimientos cargados*, pero no se halló forma de contarlos desde los 3 endpoints disponibles.

## Pistas / hipótesis para retomar

- **El timestamp `202459` es hardcodeado y constante** → el seed usa un script de datos fijos.
  Investigar si ese valor (o la fecha completa) codifica algo, o si hay una relación con los
  conteos `2576 / 3104 / 1897` (suma visible = **7577**).
- Confirmar si el conteo usa un **`categoria_id` interno** (1–20) en vez del string: probar
  **mass assignment** de `categoria_id` / `cat_id` / `id_categoria` con valores 18/19/20 en
  `/alta`, por si permite crear un proveedor apuntando a una categoría restringida.
- Revisar si falta **contexto del reto** en la plataforma (adjunto, fuente, enunciado extendido).

## Archivos

- [`turbo_movimientos.py`](./turbo_movimientos.py) — script de Turbo Intruder (Burp) que
  enumera proveedores leyendo el flash del `Set-Cookie`. Filtra los que tienen movimientos > 0.
  Ajustar el `Host` del request base a la instancia vigente.

<!-- TODO: revisar — desafío sin resolver; falta hallar cómo contar los movimientos de las 3 categorías restringidas. -->
