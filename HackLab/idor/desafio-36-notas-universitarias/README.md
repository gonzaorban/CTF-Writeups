# Desafío 36 - Notas Universitarias

Desafío 36 - Notas Universitarias 
Las credenciales del superusuario no han sido modificadas desde la instalación entonces 
entramos como admin admin 
 
Modificamos la nota de Sosa, Benjamín para que envíe un POST al Burp Suite.

![Desafío 36 - Notas Universitarias - imagen 1](images/01.png)

Identificamos que el id del estudiante es 8 y el id de la materia es 7, como queremos probar 
con todas las materias vamos hacer un ataque 
 
 
Click derecho y presionamos Sent to Intruder

![Desafío 36 - Notas Universitarias - imagen 2](images/02.png)

![Desafío 36 - Notas Universitarias - imagen 3](images/03.png)

![Desafío 36 - Notas Universitarias - imagen 4](images/04.png)

Modificamos el id de la materia que es 7 y ponemos ADD 
 
 
Y aca modifique el tipo de dato en Payload type poniendo Numbers y que sea desde From 
1 a To 50 para abarcar la mayor cantidad de ids. Para ver si alguno coincide

![Desafío 36 - Notas Universitarias - imagen 5](images/05.png)

![Desafío 36 - Notas Universitarias - imagen 6](images/06.png)

660b416167e7fd839bc06c61bb5a184b 
 
La conclusión es que todo eso que te da del token y demás es solo para confundir ya que 
no lo utilizamos. Pudimos entrar a la lista negra con el POST pero no sirvió de nada

![Desafío 36 - Notas Universitarias - imagen 7](images/07.png)

![Desafío 36 - Notas Universitarias - imagen 8](images/08.png)
