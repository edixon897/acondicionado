from app import app, request, flash, redirect, session,  render_template, url_for
from route.seguridad import login_required
from conexion import create_connection, close_connection

@app.route('/agregarUsuario', methods=['GET', 'POST'])
@login_required
def agregarUsuario():
    connection = create_connection()
    if connection is None:
        print("No hay conexión con la base de datos")
        return None
    try:
        if request.method == 'POST':
            nombre = request.form['nombre']
            apellido = request.form['apellido']
            contraseña = request.form['contraseña2']
            repetir_nueva_contraseña = request.form['contraseña3']

            if contraseña != repetir_nueva_contraseña:
                flash('La nueva contraseña y la confirmación no coinciden', 'danger')
                return redirect(url_for('agregarUsuario'))


            
            cursor = connection.cursor()
            cursor.execute(f"INSERT INTO `usuario`(`nombre`, `apellido`, `contrasena`, `rol`, `estado`) VALUES  ('{nombre}', '{apellido}','{contraseña}', 'usuario', 'Activo')")
            connection.commit()
            cursor.close()
            connection.close()
            
            flash('Usuario registrado exitosamente', 'success')
            return redirect(url_for('inicio'))
        
    except Exception as e:
        print(f"Error al consultar usuarios: {e}")
        return None
    
    finally:
        close_connection(connection)    

    return render_template('agregar_usuario.html', username=session.get('username'), rol=session.get('rol'))

