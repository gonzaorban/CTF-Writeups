# Desafío 36 - Notas Universitarias

## Análisis

Las credenciales del superusuario no han sido modificadas desde la instalación, por lo que se puede entrar con `admin` / `admin`.

## Explotación

Se modifica la nota de Sosa, Benjamín para que envíe un POST a Burp Suite.

![Desafío 36 - Notas Universitarias - imagen 1](images/01.png)

Se identifica que el ID del estudiante es `8` y el ID de la materia es `7`. Para probar con todas las materias se realiza un ataque con Intruder.

Se hace click derecho → **Send to Intruder**.

![Desafío 36 - Notas Universitarias - imagen 2](images/02.png)

![Desafío 36 - Notas Universitarias - imagen 3](images/03.png)

![Desafío 36 - Notas Universitarias - imagen 4](images/04.png)

Se marca el ID de la materia (`7`) como payload y se presiona **Add $**.

![Desafío 36 - Notas Universitarias - imagen 5](images/05.png)

Se configura **Payload type: Numbers**, de `1` a `50`, para abarcar la mayor cantidad de IDs posibles.

![Desafío 36 - Notas Universitarias - imagen 6](images/06.png)

> **Conclusión:** todo lo relacionado con tokens y demás era para confundir. La vulnerabilidad se explotó directamente modificando el ID de la materia vía IDOR.

## Flag

```
660b416167e7fd839bc06c61bb5a184b
```

![Desafío 36 - Notas Universitarias - imagen 7](images/07.png)

![Desafío 36 - Notas Universitarias - imagen 8](images/08.png)
