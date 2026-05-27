# Desafío 18 - Votación nueva versión (HackLab 2023)

## Análisis

A diferencia del desafío anterior, al borrar la cookie de voto el servidor rechaza igualmente porque verifica la IP del votante. La aplicación está detrás de Cloudflare y usa el header `X-Forwarded-For` para obtener la IP real del cliente.

## Explotación

Al enviar el POST sin la cookie de voto, aparece el mensaje de que ya se votó desde la misma IP.

![Desafío 18 - Votación nueva versión (HackLab 2023) - imagen 1](images/01.png)

![Desafío 18 - Votación nueva versión (HackLab 2023) - imagen 2](images/02.png)

**Estrategia: IP Spoofing vía `X-Forwarded-For`**

Se agrega el header falso:

```http
X-Forwarded-For: 1.1.1.1
```

> La aplicación ni siquiera valida que sea una IP con formato válido; solo verifica que sea distinta a la anterior.

Se arma una lista con distintas IPs iterando el valor del header hasta alcanzar la cantidad de votos requerida.

![Desafío 18 - Votación nueva versión (HackLab 2023) - imagen 3](images/03.png)

![Desafío 18 - Votación nueva versión (HackLab 2023) - imagen 4](images/04.png)

![Desafío 18 - Votación nueva versión (HackLab 2023) - imagen 5](images/05.png)

### Solución alternativa (Matías Sampieri)

Se puede usar otra herramienta más rápida y trabajar en simultáneo desde la misma red o distintas redes para dividir el ataque entre varios equipos.

```
IP del colaborador: [IP de la otra computadora en la red]
```

![Desafío 18 - Votación nueva versión (HackLab 2023) - imagen 7](images/07.png)

![Desafío 18 - Votación nueva versión (HackLab 2023) - imagen 8](images/08.png)

## Flag

```
143885b3abc1012375b3846f84c39203
```
