# Desafío 12 - Votación

## Análisis

La aplicación agrega una cookie `voto` después del primer voto para impedir votar nuevamente. La vulnerabilidad está en que si se omite esa cookie en el POST, el servidor acepta el voto igualmente.

## Explotación

Se realiza una votación y se intercepta el POST con Burp Suite. Se observa la cookie:

```
PHPSESSID=7a89e24b236086be28299ce7e7625ebd; voto=s8fvks7dk3ncq0
```

![Desafío 12 - Votación - imagen 1](images/01.png)

![Desafío 12 - Votación - imagen 2](images/02.png)

Se envía el mismo POST **sin la cookie `voto`** → el servidor permite el voto adicional.

Para enviar múltiples votos se usa Burp Intruder configurado con **Type: Random** y la cantidad de iteraciones deseada.

![Desafío 12 - Votación - imagen 3](images/03.png)

> La versión Community de Burp Suite tiene limitaciones de velocidad en Intruder. La solución alternativa fue ejecutar múltiples instancias en simultáneo.

![Desafío 12 - Votación - imagen 4](images/04.png)

![Desafío 12 - Votación - imagen 5](images/05.png)

![Desafío 12 - Votación - imagen 6](images/06.png)

![Desafío 12 - Votación - imagen 7](images/07.png)
