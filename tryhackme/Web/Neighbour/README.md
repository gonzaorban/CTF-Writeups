# 🕵️ Vecino

**Plataforma:** TryHackMe  
**Categoría:** Web Exploitation  
**Vulnerabilidad:** Insecure Direct Object Reference (IDOR) / Broken Access Control    
**Dificultad:** Fácil  

## 1. Reconocimiento
Al acceder a la aplicación web, nos encontramos con un panel de inicio de sesión. Inspeccionando el código fuente (`Ctrl + U`), encontramos credenciales hardcodeadas en un comentario HTML.

## 2. Análisis de Vulnerabilidad
Tras iniciar sesión con `guest:guest`, observamos que la URL contiene un parámetro directo que referencia al usuario actual:

`http://MACHINE_IP/profile?user=guest`

Esto sugiere una vulnerabilidad de **Insecure Direct Object Reference (IDOR)**. La aplicación confía en el parámetro de la URL para mostrar la información del perfil sin validar si el usuario autenticado tiene permisos para ver ese objeto.

## 3. Explotación
Para confirmar la vulnerabilidad, modificamos el parámetro `user` en la URL, cambiándolo de `guest` a `admin` (usuario mencionado en los comentarios del código fuente).

**Payload:**
```http```
GET /profile?user=admin

## 4. Resultado

El servidor devolvió el perfil del administrador, el cual contenía la bandera


## 🛡️ Remediación (Developer Perspective)
Para corregir esto en el Backend:

No confiar en el input del usuario para referencias a objetos de base de datos.

Implementar Middleware de Autorización que verifique si req.user.id coincide con el recurso solicitado.

Usar IDs aleatorios (UUIDs) en lugar de nombres secuenciales o predecibles.
