from app import request, render_template, session, flash, redirect, url_for, app
from route.seguridad import login_required
from conexion import create_connection


@app.route('/cambiar_contraseña', methods=['GET', 'POST'])
@login_required
def cambiar_contraseña():
    if request.method == 'POST':
        nombre = session['username']  
        contraseña_actual = request.form['contraseña1']
        nueva_contraseña = request.form['contraseña2']
        repetir_nueva_contraseña = request.form['contraseña3']

        if nueva_contraseña != repetir_nueva_contraseña:
            flash('La nueva contraseña y la confirmación no coinciden', 'danger')
            return redirect(url_for('cambiar_contraseña'))

        connection = create_connection()
        if connection is None:
            print("No hay conexión con la base de datos")
            return None
        cursor = connection.cursor()
        cursor.execute('SELECT contrasena FROM usuario WHERE nombre = %s AND contrasena = %s',  (nombre, contraseña_actual,))
        user = cursor.fetchone()
        cursor.close()

        if user:


            connection = create_connection()
            if connection is None:

                return None
            cursor = connection.cursor()
            cursor.execute('UPDATE usuario  SET contrasena = %s WHERE nombre = %s', (nueva_contraseña, nombre))
            connection.commit()
            cursor.close()

            flash('Contraseña actualizada exitosamente', 'success')
            return redirect(url_for('login'))
        else:
            flash('La contraseña actual es incorrecta', 'danger')

    return render_template('cambiar_contraseña.html', username=session['username'], rol = session['rol'], destino = session['destino'])
