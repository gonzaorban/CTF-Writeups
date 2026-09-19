# Desafío 33 - ECommerce (HackLab 2024)

**Plataforma:** HackLab (SoftwareSeguro)  
**Edición:** HackLab 2024  
**Categoría:** Auth  

## Análisis

El sistema tiene autenticación en dos pasos para el usuario Juan. La vulnerabilidad permite modificar el email de otro usuario (sin autenticación adicional) a través de un endpoint de perfil mal protegido.

## Explotación

Se hace login con Juan y con María para obtener sus IDs.

Login Juan → `unique_id`: `fbbd1dd9-0cca-4c91-8d2e-94015429b445` (nuevo en cada login)

![Desafío 33 - ECommerce (HackLab 2024) - imagen 1](assets/01.png)

![Desafío 33 - ECommerce (HackLab 2024) - imagen 2](assets/02.png)

![Desafío 33 - ECommerce (HackLab 2024) - imagen 3](assets/03.png)

Analizando las respuestas de login, se identifica que el ID de María es `2`.

![Desafío 33 - ECommerce (HackLab 2024) - imagen 4](assets/04.png)

![Desafío 33 - ECommerce (HackLab 2024) - imagen 5](assets/05.png)

![Desafío 33 - ECommerce (HackLab 2024) - imagen 6](assets/06.png)

Juan tiene verificación en dos pasos. Se intentó pasar el código incorrecto, poner `u: null`, y agregar campos para forzar acceso válido — nada funcionó.

![Desafío 33 - ECommerce (HackLab 2024) - imagen 7](assets/07.png)

![Desafío 33 - ECommerce (HackLab 2024) - imagen 8](assets/08.png)

![Desafío 33 - ECommerce (HackLab 2024) - imagen 9](assets/09.png)

Desde la cuenta de María, en la pestaña de perfil hay un botón deshabilitado. Al interceptar el GET del perfil se obtiene la estructura de datos.

![Desafío 33 - ECommerce (HackLab 2024) - imagen 10](assets/10.png)

![Desafío 33 - ECommerce (HackLab 2024) - imagen 11](assets/11.png)

Se prueba un POST → error. Se prueba un **PUT** con todos los datos del JSON → también error. Al **borrar el campo `username`** del PUT, la petición es aceptada.

![Desafío 33 - ECommerce (HackLab 2024) - imagen 12](assets/12.png)

![Desafío 33 - ECommerce (HackLab 2024) - imagen 13](assets/13.png)

![Desafío 33 - ECommerce (HackLab 2024) - imagen 14](assets/14.png)

![Desafío 33 - ECommerce (HackLab 2024) - imagen 15](assets/15.png)

Se modifica el email del usuario Juan (ID `1`) usando este endpoint, cambiándolo por un email propio. Al volver a ingresar con Juan, llega el código de verificación en dos pasos al email modificado.

![Desafío 33 - ECommerce (HackLab 2024) - imagen 16](assets/16.png)

![Desafío 33 - ECommerce (HackLab 2024) - imagen 17](assets/17.png)

Se completa la autenticación de Juan y se realiza la compra del producto requerido: **Memoria RAM 16GB DDR4**.

![Desafío 33 - ECommerce (HackLab 2024) - imagen 18](assets/18.png)

![Desafío 33 - ECommerce (HackLab 2024) - imagen 19](assets/19.png)

![Desafío 33 - ECommerce (HackLab 2024) - imagen 20](assets/20.png)

![Desafío 33 - ECommerce (HackLab 2024) - imagen 21](assets/21.png)

![Desafío 33 - ECommerce (HackLab 2024) - imagen 22](assets/22.png)

![Desafío 33 - ECommerce (HackLab 2024) - imagen 23](assets/23.png)

![Desafío 33 - ECommerce (HackLab 2024) - imagen 24](assets/24.png)
