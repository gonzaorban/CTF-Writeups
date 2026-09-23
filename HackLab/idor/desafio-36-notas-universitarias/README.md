# Desafío 36 - Notas Universitarias

**Plataforma:** HackLab (SoftwareSeguro)  
**Categoría:** IDOR  

## Análisis

Las credenciales del superusuario no han sido modificadas desde la instalación, por lo que se puede entrar con `admin` / `admin`.

## Explotación

Se modifica la nota de Sosa, Benjamín para que envíe un POST a Burp Suite.

![Desafío 36 - Notas Universitarias - imagen 1](assets/01.png)

Se identifica que el ID del estudiante es `8` y el ID de la materia es `7`. Para probar con todas las materias se realiza un ataque con Intruder.

Se hace click derecho → **Send to Intruder**.

![Desafío 36 - Notas Universitarias - imagen 2](assets/02.png)

![Desafío 36 - Notas Universitarias - imagen 3](assets/03.png)

![Desafío 36 - Notas Universitarias - imagen 4](assets/04.png)

Se marca el ID de la materia (`7`) como payload y se presiona **Add $**.

![Desafío 36 - Notas Universitarias - imagen 5](assets/05.png)

Se configura **Payload type: Numbers**, de `1` a `50`, para abarcar la mayor cantidad de IDs posibles.

![Desafío 36 - Notas Universitarias - imagen 6](assets/06.png)

## Flag

```
660b416167e7fd839bc06c61bb5a184b
```

![Desafío 36 - Notas Universitarias - imagen 7](assets/07.png)

> **Conclusión:** todo lo relacionado con tokens y demás era para confundir. La vulnerabilidad se explotó directamente modificando el ID de la materia vía IDOR.

![Desafío 36 - Notas Universitarias - imagen 8](assets/08.png)
