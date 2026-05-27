# Desafío 33 - ECommerce (HackLab 2024)

## Análisis

El sistema tiene autenticación en dos pasos para el usuario Juan. La vulnerabilidad permite modificar el email de otro usuario (sin autenticación adicional) a través de un endpoint de perfil mal protegido.

## Explotación

Se hace login con Juan y con María para obtener sus IDs.

Login Juan → `unique_id`: `fbbd1dd9-0cca-4c91-8d2e-94015429b445` (nuevo en cada login)

![Desafío 33 - ECommerce (HackLab 2024) - imagen 1](images/01.png)

![Desafío 33 - ECommerce (HackLab 2024) - imagen 2](images/02.png)

![Desafío 33 - ECommerce (HackLab 2024) - imagen 3](images/03.png)

Analizando las respuestas de login, se identifica que el ID de María es `2`.

![Desafío 33 - ECommerce (HackLab 2024) - imagen 4](images/04.png)

![Desafío 33 - ECommerce (HackLab 2024) - imagen 5](images/05.png)

![Desafío 33 - ECommerce (HackLab 2024) - imagen 6](images/06.png)

Juan tiene verificación en dos pasos. Se intentó pasar el código incorrecto, poner `u: null`, y agregar campos para forzar acceso válido — nada funcionó.

![Desafío 33 - ECommerce (HackLab 2024) - imagen 7](images/07.png)

![Desafío 33 - ECommerce (HackLab 2024) - imagen 8](images/08.png)

![Desafío 33 - ECommerce (HackLab 2024) - imagen 9](images/09.png)

Desde la cuenta de María, en la pestaña de perfil hay un botón deshabilitado. Al interceptar el GET del perfil se obtiene la estructura de datos.

![Desafío 33 - ECommerce (HackLab 2024) - imagen 10](images/10.png)

![Desafío 33 - ECommerce (HackLab 2024) - imagen 11](images/11.png)

Se prueba un POST → error. Se prueba un **PUT** con todos los datos del JSON → también error. Al **borrar el campo `username`** del PUT, la petición es aceptada.

![Desafío 33 - ECommerce (HackLab 2024) - imagen 12](images/12.png)

![Desafío 33 - ECommerce (HackLab 2024) - imagen 13](images/13.png)

![Desafío 33 - ECommerce (HackLab 2024) - imagen 14](images/14.png)

![Desafío 33 - ECommerce (HackLab 2024) - imagen 15](images/15.png)

Se modifica el email del usuario Juan (ID `1`) usando este endpoint, cambiándolo por un email propio. Al volver a ingresar con Juan, llega el código de verificación en dos pasos al email modificado.

![Desafío 33 - ECommerce (HackLab 2024) - imagen 16](images/16.png)

![Desafío 33 - ECommerce (HackLab 2024) - imagen 17](images/17.png)

Se completa la autenticación de Juan y se realiza la compra del producto requerido: **Memoria RAM 16GB DDR4**.

![Desafío 33 - ECommerce (HackLab 2024) - imagen 18](images/18.png)

![Desafío 33 - ECommerce (HackLab 2024) - imagen 19](images/19.png)

![Desafío 33 - ECommerce (HackLab 2024) - imagen 20](images/20.png)

![Desafío 33 - ECommerce (HackLab 2024) - imagen 21](images/21.png)

![Desafío 33 - ECommerce (HackLab 2024) - imagen 22](images/22.png)

![Desafío 33 - ECommerce (HackLab 2024) - imagen 23](images/23.png)

![Desafío 33 - ECommerce (HackLab 2024) - imagen 24](images/24.png)
