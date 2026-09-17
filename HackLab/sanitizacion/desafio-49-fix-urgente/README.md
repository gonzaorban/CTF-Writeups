# Desafío 49 - Fix Urgente

**Plataforma:** HackLab (SoftwareSeguro)  
**Categoría:** Sanitización  

Sistema de inscripciones a eventos saturado por registros falsos que agotan los cupos. El objetivo es endurecer el endpoint `inscribirse(datos)` para frenar inscripciones masivas no legítimas, validar los datos y cubrir vectores adicionales, sin tocar los parámetros de entrada ni el formato del JSON de salida.

Restricciones de la plataforma: máximo 100 líneas y 5000 caracteres; palabras prohibidas `import`, `compile`, `__`, `globals`, `lambda`, `type`, `isinstance`; solo se pueden usar los nombres inyectados por el sandbox (`datetime`, `usuarios`).

## Código original

```python
def existe_usuario(email):
    global usuarios
    return any(usuario['email'] == email for usuario in usuarios)

# path /inscribirse
def inscribirse(datos):
    try:
        if not datos:
            return {'error': 'No se proporcionó JSON'}, 400

        nombre_completo = datos.get('nombre_completo', '').strip()
        email = datos.get('email', '').strip()
        contraseña = datos.get('contraseña', '')

        if not nombre_completo or not email or not contraseña:
            return {'error': 'Los campos nombre, email y contraseña son obligatorios'}, 400

        if existe_usuario(email):
            return {'error': 'El email ya está registrado'}, 400

        nuevo_usuario = {
            'id': len(usuarios) + 1,
            'nombre_completo': nombre_completo,
            'email': email,
            'contraseña': contraseña,
            'fecha_registro': datetime.now().isoformat()
        }

        usuarios.append(nuevo_usuario)

        return {
            'mensaje': 'Usuario registrado exitosamente',
            'usuario': {
                'id': nuevo_usuario['id'],
                'nombre_completo': nuevo_usuario['nombre_completo'],
                'email': nuevo_usuario['email'],
                'fecha_registro': nuevo_usuario['fecha_registro']
            }
        }, 201

    except Exception as e:
        return {'error': f'Error interno del servidor: {str(e)}'}, 500
```

## Vulnerabilidades del código original

1. **Sin rate limiting**: registros masivos ilimitados que agotan los cupos.
2. **Duplicados evadibles**: la comparación de emails no normalizaba mayúsculas ni alias (`user+1@gmail.com`, puntos en el local de Gmail).
3. **Sin validación de formato ni longitud** de nombre, email y contraseña: habilita XSS almacenado y DoS por payloads grandes.
4. **Error 500 con tipos inesperados**: `.strip()` sobre valores no string, o un payload que no es dict.
5. **Filtración de información interna**: los errores exponían `str(e)`.
6. **Contraseñas en texto plano**.
7. **IDs con `len(usuarios) + 1`**: se repiten al borrar usuarios.

## Solución implementada

### Rate limiting por ventana deslizante

Ventana de 60 segundos con máximo de 10 registros exitosos. Se descartan los timestamps fuera de la ventana en cada llamada.

```python
WINDOW_SECONDS, MAX_REGISTRATIONS = 60, 10
registrations = []  # timestamps of successful registrations

def rate_limited():
    global registrations
    now = datetime.now().timestamp()
    registrations = [t for t in registrations if now - t < WINDOW_SECONDS]
    return len(registrations) >= MAX_REGISTRATIONS
```

### Canonicalización de email contra duplicados

Se normaliza a minúsculas, se descarta el sufijo `+alias` y se eliminan los puntos del local solo en Gmail. La deduplicación compara la forma canónica.

```python
def canonical_email(email):
    local, sep, domain = email.lower().rpartition('@')
    local = local.split('+')[0]
    if domain == 'gmail.com':
        local = local.replace('.', '')  # Gmail ignores dots in the local part
    return local + sep + domain
```

### Validación de nombre, email y contraseña

Nombre: 3–100 caracteres, entre 2 y 4 palabras, cada palabra de al menos 2 caracteres, empezando por letra y con un conjunto de caracteres restringido (evita inyección de marcado).

```python
NAME_CHARS = set("abcdefghijklmnopqrstuvwxyzáéíóúüñ'-")

def valid_name(name):
    words = name.split(' ')
    return (3 <= len(name) <= 100 and 2 <= len(words) <= 4
            and all(len(w) >= 2 and w[0].isalpha() and set(w.lower()) <= NAME_CHARS for w in words))
```

Email: longitud máxima 254, un único `@`, charset acotado, local de hasta 64 caracteres, sin puntos consecutivos ni al borde, TLD alfabético y bloqueo de dominios desechables.

```python
def valid_email(email):
    if len(email) > 254 or email.count('@') != 1 or not set(email.lower()) <= EMAIL_CHARS:
        return False
    local, domain = email.split('@')
    parts = domain.split('.')
    return (0 < len(local) <= 64 and '..' not in email and local[0] != '.' and local[-1] != '.'
            and len(parts) > 1 and all(p and p[0] != '-' and p[-1] != '-' for p in parts)
            and parts[-1].isalpha() and len(parts[-1]) > 1 and domain not in DISPOSABLE_DOMAINS)
```

Contraseña: 8–128 caracteres con mayúscula, minúscula y dígito.

```python
def strong_password(pwd):
    return (8 <= len(pwd) <= 128 and any(c.islower() for c in pwd)
            and any(c.isupper() for c in pwd) and any(c.isdigit() for c in pwd))
```

### Manejo de entrada y errores

Se validan tipos antes de operar sobre strings, se colapsan espacios internos del nombre, los mensajes de error son genéricos y el `except` global evita filtrar detalles y responde 500 controlado.

```python
if not all(str(v) == v and len(v) <= 300 for v in (name, email, password)):
    return {'error': 'Formato de datos inválido'}, 400
name, email = ' '.join(name.split()), email.strip()
```

### IDs robustos

El ID se calcula como el máximo existente más uno, ignorando IDs no numéricos, para evitar colisiones tras borrados.

```python
ids = [int(u.get('id')) for u in usuarios if str(u.get('id')).isdigit()] + [0]
nuevo_usuario = {'id': max(ids) + 1, ...}
```

## Lección aprendida (proceso de resolución)

Al principio la plataforma solo devolvía "El código no es seguro", sin detalle. Iteré a ciegas agregando defensas cada vez más agresivas —heurísticas anti-bot, límites de ráfaga, blacklist amplia— y eso rompía registros legítimos. **Sobrecorregir rompe la funcionalidad.**

Analizando la response con Burp Suite aparecieron 14 tests unitarios: `test_inscribirse_ok`, `test_inscribirse_sin_datos`, `test_campos_faltantes`, `test_nombre_corto`, `test_nombre_largo`, `test_nombre_invalido`, `test_nombre_sin_apellido`, `test_nombre_demasiadas_palabras`, `test_email_invalido`, `test_email_largo`, `test_email_duplicado`, `test_password_corta`, `test_password_larga`, `test_password_sin_complejidad`. **Conviene buscar feedback detallado antes de iterar a ciegas.**

Con un cambio por envío para aislar cada efecto:

- `example.com` estaba bloqueado, siendo un dominio típico de datos de prueba: lo desbloqueé y dejé la blacklist acotada a dominios desechables reales.
- `test_nombre_demasiadas_palabras` pasaba por accidente: otra heurística rechazaba el nombre y el error genérico ocultaba el motivo real. El límite correcto es de 4 palabras. **Un error genérico puede enmascarar falsos positivos.**
- `test_inscribirse_ok` y `test_email_duplicado` fallaban por el hashing. Con un valor fijo pasaron; con `secrets` + `hashlib.sha256`, con PBKDF2 y con `hashlib.sha256` sin salt, fallaron. Conclusión: **`hashlib` no está disponible en el sandbox**, por lo que `hash_password` queda como placeholder de diagnóstico —no seguro— para no bloquear los tests. En producción debe reemplazarse por un hash con sal y función lenta.

```python
def hash_password(pwd):
    return 'diagnostic-only'  # NOT secure: hashlib is unavailable in the sandbox
```

**Aislar un solo cambio por envío** fue lo que permitió atribuir cada fallo a su causa.

## Flag

![Desafío 49 - Fix Urgente - imagen 1](assets/01.png)

```
30ed2eec1a72f0dc1fdc29bcf4626652
```
