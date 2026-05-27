# Desafío 12 - Votación

Broken Access Control 
Desafío 12 - Votación 
 
Realizó una votación y veo que cuando quiero ejecutar la segunda no me deja porque se 
agrega una cookie de voto 
Analizo un POST y veo que tiene  
PHPSESSID=7a89e24b236086be28299ce7e7625ebd;  
voto=s8fvks7dk3ncq0

![Desafío 12 - Votación - imagen 1](images/01.png)

![Desafío 12 - Votación - imagen 2](images/02.png)

Por lo que chat después de muchos prompt me tiro la gran idea de enviar el mismo POST 
pero sin el voto y ahí me permitió realizar más de un voto. Esto funciona debido a un error 
del Desarrollador. 
 
Entonces ahora el problema sería enviar muchos votos. 
 
Chusmeando pude hacer que se envíe muchas veces configurando así, en How Many iría la 
cantidad y tenes que poner Type Random sino no te deja.

![Desafío 12 - Votación - imagen 3](images/03.png)

Estuve navegando por toda la configuración de Burp Suite y nada me sirvio como tal, 
incluso me tuve que descargar la extensión Turbo Intruder(no me sirvio de nada porque no 
pude ejecutarla como tal) 
 
 
 
Y la conclusión que llegué es que hay que comprar la versión Pro 
 
La solución que tuve para ejecutar 3000 votos fue ejecutar en simultáneo como un bruto, 
porque la configuración de procesos concurrentes de la aplicación parecía no funcionar:

![Desafío 12 - Votación - imagen 4](images/04.png)

![Desafío 12 - Votación - imagen 5](images/05.png)

![Desafío 12 - Votación - imagen 6](images/06.png)

![Desafío 12 - Votación - imagen 7](images/07.png)
