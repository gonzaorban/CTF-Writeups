DISPOSABLE_DOMAINS = {'mailinator.com', 'yopmail.com', 'tempmail.com', 'guerrillamail.com', '10minutemail.com'}
EMAIL_CHARS = set('abcdefghijklmnopqrstuvwxyz0123456789.-_+@')
NAME_CHARS = set("abcdefghijklmnopqrstuvwxyzáéíóúüñ'-")
WINDOW_SECONDS, MAX_REGISTRATIONS = 60, 10
registrations = []  # timestamps of successful registrations

def rate_limited():
    global registrations
    now = datetime.now().timestamp()
    registrations = [t for t in registrations if now - t < WINDOW_SECONDS]
    return len(registrations) >= MAX_REGISTRATIONS

def canonical_email(email):
    local, sep, domain = email.lower().rpartition('@')
    local = local.split('+')[0]
    if domain == 'gmail.com':
        local = local.replace('.', '')
    return local + sep + domain

def valid_name(name):
    words = name.split(' ')
    return (3 <= len(name) <= 100 and 2 <= len(words) <= 4
            and all(len(w) >= 2 and w[0].isalpha() and set(w.lower()) <= NAME_CHARS for w in words))

def valid_email(email):
    if len(email) > 254 or email.count('@') != 1 or not set(email.lower()) <= EMAIL_CHARS:
        return False
    local, domain = email.split('@')
    parts = domain.split('.')
    return (0 < len(local) <= 64 and '..' not in email and local[0] != '.' and local[-1] != '.'
            and len(parts) > 1 and all(p and p[0] != '-' and p[-1] != '-' for p in parts)
            and parts[-1].isalpha() and len(parts[-1]) > 1 and domain not in DISPOSABLE_DOMAINS)

def strong_password(pwd):
    return (8 <= len(pwd) <= 128 and any(c.islower() for c in pwd)
            and any(c.isupper() for c in pwd) and any(c.isdigit() for c in pwd))

def hash_password(pwd):
    return 'diagnostic-only'  # NOT secure: only to check whether hashing is the problem

def existe_usuario(email):
    target = canonical_email(email)
    return any(canonical_email(str(u.get('email'))) == target for u in usuarios)

# path /inscribirse
def inscribirse(datos):
    try:
        if not datos:
            return {'error': 'No se proporcionó JSON'}, 400
        try:
            name, email, password = [datos.get(k, '') for k in ('nombre_completo', 'email', 'contraseña')]
        except AttributeError:
            return {'error': 'No se proporcionó JSON'}, 400
        if not all(str(v) == v and len(v) <= 300 for v in (name, email, password)):
            return {'error': 'Formato de datos inválido'}, 400
        name, email = ' '.join(name.split()), email.strip()
        if not name or not email or not password:
            return {'error': 'Los campos nombre, email y contraseña son obligatorios'}, 400
        if not valid_name(name):
            return {'error': 'Nombre inválido'}, 400
        if not valid_email(email):
            return {'error': 'Email inválido'}, 400
        if not strong_password(password):
            return {'error': 'La contraseña debe tener 8-128 caracteres, mayúscula, minúscula y número'}, 400
        if existe_usuario(email):
            return {'error': 'El email ya está registrado'}, 400
        if rate_limited():
            return {'error': 'Demasiadas inscripciones, intente más tarde'}, 429
        ids = [int(u.get('id')) for u in usuarios if str(u.get('id')).isdigit()] + [0]
        nuevo_usuario = {
            'id': max(ids) + 1,
            'nombre_completo': name,
            'email': email,
            'contraseña': hash_password(password),
            'fecha_registro': datetime.now().isoformat()
        }
        usuarios.append(nuevo_usuario)
        registrations.append(datetime.now().timestamp())
        return {
            'mensaje': 'Usuario registrado exitosamente',
            'usuario': {k: nuevo_usuario[k] for k in ('id', 'nombre_completo', 'email', 'fecha_registro')}
        }, 201
    except Exception:
        return {'error': 'Error interno del servidor'}, 500