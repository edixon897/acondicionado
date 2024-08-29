from app import app, request, flash, redirect, generate_password_hash, session, sqlite3, render_template, url_for
from route.seguridad import login_required
from conexion import mydb

@app.route('/agregarUsuario', methods=['GET', 'POST'])
@login_required
def agregarUsuario():
    if request.method == 'POST':
        nombre = request.form['nombre']
        apellido = request.form['apellido']
        contraseña = request.form['contraseña2']
        repetir_nueva_contraseña = request.form['contraseña3']
        rol = request.form.get('rol')  

        if contraseña != repetir_nueva_contraseña:
            flash('La nueva contraseña y la confirmación no coinciden', 'danger')
            return redirect(url_for('agregarUsuario'))


        mydb.connect()
        cursor = mydb.cursor()
        cursor.execute(f"INSERT INTO `usuario`(`nombre`, `apellido`, `contrasena`, `rol`, `estado`) VALUES  ('{nombre}', '{apellido}','{contraseña}', 'usuario', 'Activo')")
        mydb.commit()
        cursor.close()
        mydb.close()
        
        flash('Usuario registrado exitosamente', 'success')
        return redirect(url_for('inicio'))

    return render_template('agregar_usuario.html', username=session.get('username'), rol=session.get('rol'))

