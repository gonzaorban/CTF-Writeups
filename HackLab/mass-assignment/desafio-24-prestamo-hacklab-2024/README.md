# Desafío 24 - Préstamo (HackLab 2024)

**Plataforma:** HackLab (SoftwareSeguro)  
**Edición:** HackLab 2024  
**Categoría:** Mass Assignment  

## Análisis

El servidor expone los indicadores de puntaje en un GET. Al modificar directamente el valor a 100 el usuario es bloqueado, por lo que hay que incrementar los valores de a uno hasta llegar al máximo.

## Explotación

Se intercepta el GET de los indicadores y se analiza la estructura de la respuesta.

![Desafío 24 - Préstamo (HackLab 2024) - imagen 1](assets/01.png)

![Desafío 24 - Préstamo (HackLab 2024) - imagen 2](assets/02.png)

![Desafío 24 - Préstamo (HackLab 2024) - imagen 3](assets/03.png)

Se configura un ataque con Intruder iterando el valor del indicador de `From: (valor_actual + 1)` hasta `To: 100` para cada indicador.

![Desafío 24 - Préstamo (HackLab 2024) - imagen 4](assets/04.png)

![Desafío 24 - Préstamo (HackLab 2024) - imagen 5](assets/05.png)

Se confirma que la modificación fue exitosa y se repite el proceso para cada indicador.

![Desafío 24 - Préstamo (HackLab 2024) - imagen 6](assets/06.png)

![Desafío 24 - Préstamo (HackLab 2024) - imagen 7](assets/07.png)

![Desafío 24 - Préstamo (HackLab 2024) - imagen 8](assets/08.png)

## Flag

```
85b952b272b0de1997b0d8360f42ade8
```

![Desafío 24 - Préstamo (HackLab 2024) - imagen 9](assets/09.png)
