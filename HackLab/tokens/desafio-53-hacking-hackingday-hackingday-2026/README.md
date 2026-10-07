# Desafío 53 - Hacking HackingDay

**Plataforma:** HackLab (SoftwareSeguro)

**Edición:** HackingDay 2026

**Categoría:** Tokens

**Herramientas:** Burp Suite (Repeater), jwt.io

## Enunciado

Tu amigo se inscribió a HackingDay 2026 y estuvo chusmeando a ver si encontraba alguna forma de obtener una lista de todos los que se anotaron. Encontró la ruta `/admin`, pero ni él ni vos tienen una cuenta con rol de administrador.

- **Aplicación:** HackingDay 2026
- **Ruta encontrada:** `/admin`
- No se dispone de una cuenta con rol de administrador.
- **Objetivo:** obtener la lista de todos los participantes registrados.

## Análisis

Para poder operar sobre la aplicación, primero hay que crear una cuenta en `/registro` (nombre, email, teléfono y contraseña). El registro genera una sesión con rol `attendee`, que es el punto de partida del ataque.

![Crear cuenta](./assets/00-crear-cuenta.png)

Al revisar DevTools → Sources no hay bundle JS propio de la app, solo el HTML de cada página. Es decir, **no es una SPA** (*Single Page Application*: una app que carga un único HTML y un bundle de JavaScript que arma las pantallas en el navegador y pide los datos a una API). Esta app está **renderizada en el servidor**: cada página (`/`, `/perfil`, `/admin`) es HTML que arma el backend. Eso significa que el control de acceso es 100% server-side —no hay lógica de permisos en el cliente que se pueda saltear—, así que el servidor necesita identificar al usuario en cada request. Para eso usa un **JWT** guardado en la cookie `session`, donde viaja el rol.

La sesión viaja en la cookie `session`, que es un JWT:

![Request con la cookie session](./assets/06-request-cookie-session.png)

```
eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzeXN0ZW1fZGF0YSI6eyJ1c2VyX2lkIjoxOCwidXNlcl9yb2xlIjoiYXR0ZW5kZWUifSwidXNlcl9kYXRhIjp7Im5hbWUiOiJnb256YSIsInBob25lIjoiMzYyNCJ9LCJleHAiOjE3OTEzNzI4MTN9.k8qQj1oIat1ksiyRl5zJaN253jEAj-PPdQK_1iThiP8
```

Ese token (`alg: HS256`) decodifica así:

![Token decodificado](./assets/07-token-decodificado.png)

El diseño separa a propósito dos objetos:

- **`system_data`** → lo que controla el servidor: `user_id` y `user_role`.
- **`user_data`** → lo que edita el usuario: `name` y `phone`.

La pantalla **Mi perfil** (`/perfil`) muestra el rol actual (`attendee`) y guarda cambios con una llamada a la API:

![Perfil con rol attendee](./assets/01-perfil-rol-attendee.png)

```http
POST /api/perfil
Content-Type: application/json

{"name":"gonza","phone":"3624"}
```

La respuesta es `200 {"ok":true}` y trae un **`Set-Cookie: session=...` con un JWT nuevo re-firmado por el servidor**. Es decir: el servidor conoce el secreto HMAC y vuelve a firmar el token con los datos que le mandamos.

### Vector descartado

- **Forjar la firma** (`alg:none` o firma basura): el servidor valida correctamente la firma; los tokens manipulados son rechazados.

## Explotación

El fallo es un **mass assignment** combinado con una **confusión de contexto al leer el rol**. Al mandar campos extra al `POST /api/perfil`, el servidor **los copia dentro de `user_data`** y re-firma. Por ejemplo, con el body:

```json
{"name":"gonza","user_role":"admin"}
```

![Request con user_role admin](./assets/02-request-user_role-admin.png)

el token devuelto (válido y firmado por el propio servidor) queda:

![Token con user_data.user_role admin](./assets/03-token-user_data-admin.png)

El `user_role: admin` cae en `user_data`, no en `system_data`. El rol "real" sigue siendo `attendee`... **pero la validación de acceso a `/admin` lee el rol del lugar equivocado**: busca `user_role` en `user_data` (el objeto que controla el usuario) en vez de en `system_data`. Como el token está firmado por el servidor, la firma es válida y el check pasa.

Los pasos concretos:

1. En Burp Repeater, reenviar el guardado de perfil agregando el campo `user_role`:

   ```http
   POST /api/perfil
   Content-Type: application/json

   {"name":"gonza","user_role":"admin"}
   ```

2. Copiar el `session=...` del `Set-Cookie` de la respuesta (el JWT nuevo tiene `user_data.user_role: "admin"`).

3. Usar ese token como cookie `session` y navegar a `/admin`.

   ![GET /admin con el token modificado](./assets/08-get-admin-con-token.png)

El servidor acepta el token (firma válida), lee `admin` desde `user_data.user_role` y renderiza el **Panel de organización** con los 20 inscriptos (nombre, email, teléfono, rol) y la flag.

![Panel de organización](./assets/04-panel-organizacion.png)

![Flag](./assets/05-flag.png)

## Flag

```
ad440bb573835abcd8a9be26acc749d3
```

## 🛡️ Remediación (Developer Perspective)

- **Nunca derivar privilegios de datos editables por el usuario.** El rol debe leerse siempre de la fuente autoritativa (`system_data.user_role`), nunca de un campo que el usuario puede influir (`user_data`).
- **Whitelist de campos en el update de perfil.** El endpoint `/api/perfil` debe aceptar únicamente `name` y `phone` y descartar cualquier otro campo del body, en vez de volcar el objeto entero dentro de `user_data` (mass assignment).
- **No reconstruir el claim de rol a partir del input.** Al re-firmar el JWT, copiar `system_data` del token previo (o releerlo de la base) y no mezclarlo con datos que vienen del cliente.
- **Separar claims de identidad de datos de perfil** o, mejor, mantener el rol fuera del token y resolverlo server-side por `user_id` en cada request sensible.
