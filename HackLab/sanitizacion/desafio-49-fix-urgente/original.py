
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