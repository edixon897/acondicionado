from app import request, render_template, session, sqlite3, flash, check_password_hash, redirect, url_for, generate_password_hash, app
from route.seguridad import login_required


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

        conn = sqlite3.connect('usuario.db')
        c = conn.cursor()
        c.execute('SELECT contrasena FROM users WHERE nombre = ?', (nombre,))
        user = c.fetchone()
        conn.close()

        if user and check_password_hash(user[0], contraseña_actual):
            nueva_contraseña_hash = generate_password_hash(nueva_contraseña)

            conn = sqlite3.connect('usuario.db')
            c = conn.cursor()
            c.execute('UPDATE users SET contrasena = ? WHERE nombre = ?', (nueva_contraseña_hash, nombre))
            conn.commit()
            conn.close()

            flash('Contraseña actualizada exitosamente', 'success')
            return redirect(url_for('login'))
        else:
            flash('La contraseña actual es incorrecta', 'danger')

    return render_template('cambiar_contraseña.html', username=session['username'], rol = session['rol'])
