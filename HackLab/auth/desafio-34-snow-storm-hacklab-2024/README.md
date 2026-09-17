# Desafío 34 - Snow Storm (HackLab 2024)

**Plataforma:** HackLab (SoftwareSeguro)  
**Edición:** HackLab 2024  
**Categoría:** Auth  

## Análisis

Los tokens de recuperación de contraseña se generan de forma secuencial (predecible). Al pedir un token propio y crackear su valor numérico, se puede predecir el token del siguiente usuario.

## Explotación

Se identifica el email de Juan Pérez:

```
juan.perez@hacklab.com
```

![Desafío 34 - Snow Storm (HackLab 2024) - imagen 1](assets/01.png)

Se crea un nuevo usuario propio y se solicita el enlace de recuperación de contraseña. Se verifica que cada token es único por correo (enviar ambos a la vez no genera el mismo token).

![Desafío 34 - Snow Storm (HackLab 2024) - imagen 2](assets/02.png)

![Desafío 34 - Snow Storm (HackLab 2024) - imagen 3](assets/03.png)

Se intenta modificar el email directamente desde la cuenta (como en el desafío anterior) pero no está permitido.

![Desafío 34 - Snow Storm (HackLab 2024) - imagen 4](assets/04.png)

Se crackean los dos tokens recibidos, confirmando que son secuenciales. Se genera el hash para el número siguiente (`2111`):

```
1a0a283bfe7c549dee6c638a05200e32
```

Flags intermedias:

```
05546b0e38ab9175cd905eebcc6ebb76
c3535febaff29fcb7c0d20cbe94391c7
```

![Desafío 34 - Snow Storm (HackLab 2024) - imagen 5](assets/05.png)

Se copia la URL de recuperación propia y se reemplaza el token por el predicho:

```
https://chl-d984116d-5c95-4615-9ea9-42bc90e876c8-snow-storm.softwareseguro.com.ar/recovery/?t=1a0a283bfe7c549dee6c638a05200e32
```

Se establece una nueva contraseña:

```
gonzaaa123*
```

![Desafío 34 - Snow Storm (HackLab 2024) - imagen 6](assets/06.png)

Se inicia sesión con la cuenta de Juan Pérez:

```
juan.perez@hacklab.com
gonzaaa123*
```

![Desafío 34 - Snow Storm (HackLab 2024) - imagen 7](assets/07.png)

Se cambia el nombre como indica el enunciado.

![Desafío 34 - Snow Storm (HackLab 2024) - imagen 8](assets/08.png)

![Desafío 34 - Snow Storm (HackLab 2024) - imagen 9](assets/09.png)

![Desafío 34 - Snow Storm (HackLab 2024) - imagen 10](assets/10.png)

![Desafío 34 - Snow Storm (HackLab 2024) - imagen 11](assets/11.png)

## Flag

```
17968af07cf621117b36cfbc35b51361
```

![Desafío 34 - Snow Storm (HackLab 2024) - imagen 12](assets/12.png)

![Desafío 34 - Snow Storm (HackLab 2024) - imagen 13](assets/13.png)
