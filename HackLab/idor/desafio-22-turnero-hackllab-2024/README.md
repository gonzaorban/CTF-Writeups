# Desafío 22 - Turnero (HackLab 2024)

## Análisis

Se usa Burp Suite con las herramientas **Proxy** e **Intruder**:

- **Proxy**: intercepta todo el tráfico entre el browser y el server. Hasta que no se habilita *Forward*, la página no se actualiza. Permite ver y modificar todos los headers y el cuerpo de la petición antes de enviarla.
- **Intruder**: permite automatizar peticiones modificando parámetros en un rango definido.

## Explotación

![Desafío 22 - Turnero (HackLab 2024) - imagen 1](images/01.png)

![Desafío 22 - Turnero (HackLab 2024) - imagen 2](images/02.png)

![Desafío 22 - Turnero (HackLab 2024) - imagen 3](images/03.png)

Se configura Intruder para iterar sobre el parámetro `id` y encontrar el usuario solicitado. Una clave para no revisar todas las respuestas una por una es ordenar por **Length**: los usuarios que habían pedido turnos tienen respuestas de mayor tamaño.

![Desafío 22 - Turnero (HackLab 2024) - imagen 4](images/04.png)

![Desafío 22 - Turnero (HackLab 2024) - imagen 5](images/05.png)

Se abre el usuario correcto (ID `101` en este ejercicio) y se identifican los IDs de sus turnos (del 10 al 13) para eliminarlos luego.

Se presiona el botón **Cancelar** para enviar la petición al Burp Suite.

![Desafío 22 - Turnero (HackLab 2024) - imagen 6](images/06.png)

![Desafío 22 - Turnero (HackLab 2024) - imagen 7](images/07.png)

En la petición de cancelar el turno, el parámetro de ID del turno (que originalmente era `1`) se reemplaza por los IDs de los turnos del usuario `xdalvik` (del 10 al 13).

## Flag

Al volver a la página principal aparece el código.

![Desafío 22 - Turnero (HackLab 2024) - imagen 8](images/08.png)

![Desafío 22 - Turnero (HackLab 2024) - imagen 9](images/09.png)
