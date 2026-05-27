# Desafío 11 - Gran Rifa 2019

## Análisis

El endpoint de edición acepta campos adicionales en el JSON que no deberían ser modificables por el usuario. Al incluir `esta_pago: true` en el cuerpo del POST, el servidor lo procesa y marca la rifa como pagada.

## Explotación

Se recarga la página y se intercepta el GET en **HTTP History** de Burp Suite. Se identifica el campo `esta_pago` en la respuesta.

![Desafío 11 - Gran Rifa 2019 - imagen 1](images/01.png)

![Desafío 11 - Gran Rifa 2019 - imagen 2](images/02.png)

Se presiona **Editar** y **Guardar** para capturar el POST. Se modifica el JSON del cuerpo:

```json
{
  "comprador": "John Backus",
  "esta_pago": true
}
```

![Desafío 11 - Gran Rifa 2019 - imagen 3](images/03.png)

La petición se procesa correctamente. Se recarga la página y el estado queda como pagado.

![Desafío 11 - Gran Rifa 2019 - imagen 4](images/04.png)

## Flag

```
ed20b8f11252a75b30d594af897c3aad
```

![Desafío 11 - Gran Rifa 2019 - imagen 5](images/05.png)

![Desafío 11 - Gran Rifa 2019 - imagen 6](images/06.png)

![Desafío 11 - Gran Rifa 2019 - imagen 7](images/07.png)
