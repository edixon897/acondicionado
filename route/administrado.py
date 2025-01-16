from flask import flash
from app import render_template, session, app, logged_in_ips, redirect, url_for
from conexion import create_connection, close_connection
from route.seguridad import login_required


# Funcion para obtener las sesiones activas
def obtener_sesiones_activas():
    try:
        connection = create_connection()
        if connection is None:
            print("No hay conexión con la base de datos")
            return None
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM usuario")
        usuarios = cursor.fetchall()
    except Exception as e:
        return None 
    finally:
        close_connection(connection)

    sesiones_activas = []
    for usuario in usuarios:
        username = usuario[1]
        print('Usuario de sesion: ',username)
        ip_address = logged_in_ips.get(username, 'No disponible')  
        estado = 'Conectado' if username in logged_in_ips else 'Desconectado'  
        sesiones_activas.append({
            'id': usuario[0],
            'username': username,
            'ip_address': ip_address,
            'estado': estado,
            'estado_us': usuario[5]
        })

    return sesiones_activas
    

# Ruta para la pagina de administrador
@app.route('/administrador', methods=['GET'])
@login_required
def administrador():
    # Aseguro de que el usuario sea administrador para acceder a esta pagina
    if session.get('rol') != 'administrador':
        flash('Acceso no autorizado', 'danger')
        return redirect(url_for('inicio'))

    sesiones_activas = obtener_sesiones_activas()


    return render_template('administrador.html', sesiones_activas=sesiones_activas, rol = session['rol'], destino = session['destino'])


# Ruta para actualizar las sesiones activas
@app.route('/actualizar_sesiones_activas', methods=['GET'])
@login_required
def actualizar_sesiones_activas():
    sesiones_activas = obtener_sesiones_activas()

    return redirect('administrador', sesiones_activas=sesiones_activas)



@app.route('/cambiar_estado_usuario/<int:user_id>', methods=['POST'])
@login_required
def cambiar_estado_usuario(user_id):
    # Aseguro de que el usuario sea administrador para realizar cambios
    if session.get('rol') != 'administrador':
        flash('Acceso no autorizado', 'danger')
        return redirect(url_for('inicio'))

    
    try:
        connection = create_connection()
        if connection is None:
            print("No hay conexión con la base de datos")
            return None
        cursor = connection.cursor()

        # Obtener el estado actual del usuario
        cursor.execute("SELECT estado FROM usuario WHERE id = %s", (user_id,))
        estado_actual = cursor.fetchone()[0]

        # Cambiar el estado
        nuevo_estado = 'Inactivo' if estado_actual == 'Activo' else 'Activo'
        cursor.execute("UPDATE usuario SET estado = %s WHERE id = %s", (nuevo_estado, user_id))
        connection.commit()

        flash(f'El estado del usuario ha sido cambiado a {nuevo_estado}', 'success')
        
    except Exception as e:
        return None
    
    finally:
        close_connection(connection)

    return redirect(url_for('administrador'))




