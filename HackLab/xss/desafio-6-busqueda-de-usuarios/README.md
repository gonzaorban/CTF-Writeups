# Desafío 6 - Búsqueda de usuarios

## Análisis

El texto ingresado en el input aparece interpolado dentro de un `<h5>` como:

```html
<h5>Búsqueda: {tu_input}</h5>
```

Esto permite cerrar la etiqueta actual e inyectar nuevas etiquetas HTML sin que el backend valide ni sanitice la entrada.

## Explotación

Se envía `HOLA` por el input y se confirma que se renderiza dentro de un `<h5>`.

![Desafío 6 - Búsqueda de usuarios - imagen 1](images/01.png)

![Desafío 6 - Búsqueda de usuarios - imagen 2](images/02.png)

Se inyecta el payload requerido por el ejercicio:

```html
test</h5>
<hr>
<h5>HACKED</h5>
```

![Desafío 6 - Búsqueda de usuarios - imagen 3](images/03.png)

El payload cierra la etiqueta `<h5>` activa, inserta una línea horizontal `<hr>` y agrega un nuevo `<h5>` con el texto `HACKED`.

![Desafío 6 - Búsqueda de usuarios - imagen 4](images/04.png)

![Desafío 6 - Búsqueda de usuarios - imagen 5](images/05.png)

## Flag

```
a24fc443b7c617783d96417a4f9929dc
```
