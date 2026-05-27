# Desafío 33 - ECommerce (HackLab 2024)

Auth 
Desafío 33 - ECommerce (HackLab 2024) 
 
Login Juan 
 
Response 
 
(cada vez que inicias te da un unique_id nuevo) 
fbbd1dd9-0cca-4c91-8d2e-94015429b445 
 
Login Maria 
 
Response

![Desafío 33 - ECommerce (HackLab 2024) - imagen 1](images/01.png)

![Desafío 33 - ECommerce (HackLab 2024) - imagen 2](images/02.png)

![Desafío 33 - ECommerce (HackLab 2024) - imagen 3](images/03.png)

Response 
 
 
 
 
Response 
 
 
 
 
Response 
 
Vemos que el id de maria es 2

![Desafío 33 - ECommerce (HackLab 2024) - imagen 4](images/04.png)

![Desafío 33 - ECommerce (HackLab 2024) - imagen 5](images/05.png)

![Desafío 33 - ECommerce (HackLab 2024) - imagen 6](images/06.png)

![Desafío 33 - ECommerce (HackLab 2024) - imagen 7](images/07.png)

![Desafío 33 - ECommerce (HackLab 2024) - imagen 8](images/08.png)

![Desafío 33 - ECommerce (HackLab 2024) - imagen 9](images/09.png)

Vemos que al entrar como Juan tiene verificación en dos pasos 
 
Probamos entrar y nos dice que el código es incorrecto. Probamos poniendo el campo “u” 
en null pero nos da acceso inválido, también agregando campos para que de válido el 
acceso pero no funcionaba nada así que decidimos buscar por otro lado

![Desafío 33 - ECommerce (HackLab 2024) - imagen 10](images/10.png)

![Desafío 33 - ECommerce (HackLab 2024) - imagen 11](images/11.png)

Volviendo a la cuenta de Maria vemos que tenemos esto en la pestaña de perfil, que no te 
deja presionar el botón. ​
 
 
Pero si interceptamos la señal del profile. Podemos ver que nos devuelve los datos 
 
Request

![Desafío 33 - ECommerce (HackLab 2024) - imagen 12](images/12.png)

![Desafío 33 - ECommerce (HackLab 2024) - imagen 13](images/13.png)

![Desafío 33 - ECommerce (HackLab 2024) - imagen 14](images/14.png)

Asi que intentamos realizar un POST y nos devuelve esto 
 
 
De ahí probamos un PUT que es más adecuado agregando todos los datos en el JSON 
 
Nos devuelve esto 
 
 
Asi que borramos el username, y ahi nos devuelve que la petición es válida

![Desafío 33 - ECommerce (HackLab 2024) - imagen 15](images/15.png)

![Desafío 33 - ECommerce (HackLab 2024) - imagen 16](images/16.png)

![Desafío 33 - ECommerce (HackLab 2024) - imagen 17](images/17.png)

![Desafío 33 - ECommerce (HackLab 2024) - imagen 18](images/18.png)

![Desafío 33 - ECommerce (HackLab 2024) - imagen 19](images/19.png)

Así que ahora probamos modificar los datos de Juan que sabemos que es el usuario 1. En 
este caso como la autenticación en dos pasos indicaba que el código se enviaba al mail, 
probamos poniendo un mail de nuestra propiedad. 
 
 
Vuelvo a ingresar con el usuario y contraseña de Juan, de ahí reviso mis correo y me llega 
el código 
 
 
Realizo la compra del producto que pedía Memoria RAM 16GB DDR4

![Desafío 33 - ECommerce (HackLab 2024) - imagen 20](images/20.png)

![Desafío 33 - ECommerce (HackLab 2024) - imagen 21](images/21.png)

![Desafío 33 - ECommerce (HackLab 2024) - imagen 22](images/22.png)

![Desafío 33 - ECommerce (HackLab 2024) - imagen 23](images/23.png)

![Desafío 33 - ECommerce (HackLab 2024) - imagen 24](images/24.png)
