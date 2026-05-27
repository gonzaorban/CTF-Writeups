# Desafío 23 - Préstamo (HackLab 2024)

## Análisis

El servidor expone los indicadores de puntaje en un GET. Al modificar directamente el valor a 100 el usuario es bloqueado, por lo que hay que incrementar los valores de a uno hasta llegar al máximo.

## Explotación

Se intercepta el GET de los indicadores y se analiza la estructura de la respuesta.

![Desafío 23 - Préstamo (HackLab 2024) - imagen 1](images/01.png)

![Desafío 23 - Préstamo (HackLab 2024) - imagen 2](images/02.png)

![Desafío 23 - Préstamo (HackLab 2024) - imagen 3](images/03.png)

Se configura un ataque con Intruder iterando el valor del indicador de `From: (valor_actual + 1)` hasta `To: 100` para cada indicador.

![Desafío 23 - Préstamo (HackLab 2024) - imagen 4](images/04.png)

![Desafío 23 - Préstamo (HackLab 2024) - imagen 5](images/05.png)

Se confirma que la modificación fue exitosa y se repite el proceso para cada indicador.

![Desafío 23 - Préstamo (HackLab 2024) - imagen 6](images/06.png)

![Desafío 23 - Préstamo (HackLab 2024) - imagen 7](images/07.png)

![Desafío 23 - Préstamo (HackLab 2024) - imagen 8](images/08.png)

## Flag

```
85b952b272b0de1997b0d8360f42ade8
```

![Desafío 23 - Préstamo (HackLab 2024) - imagen 9](images/09.png)
