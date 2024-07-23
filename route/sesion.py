from app import app, session, flash, redirect, url_for, request,  check_password_hash, render_template, logged_in_ips
from route.seguridad import login_required, obtener_direccion_ip

from conexion import mydb



@app.route('/logout')
@login_required
def logout():
    if 'username' in session:
        # Eliminar la entrada del usuario del diccionario de sesiones activas
        if session['username'] in logged_in_ips:
            del logged_in_ips[session['username']]
        session.pop('logged_in', None)
        session.pop('username', None)
        session.pop('rol', None)
        flash('Has cerrado sesión', 'info')
    return redirect(url_for('login'))



@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        nombre = request.form['nombre']
        contraseña = request.form['contraseña']

        conn = mydb.connect()
        cursor = mydb.cursor()
        cursor.execute(f"SELECT nombre, contrasena, rol FROM usuario WHERE nombre = '{nombre}' and contrasena = '{contraseña}'")
        user = cursor.fetchone()
        cursor.close()

        if user:
            session['logged_in'] = True
            session['username'] = nombre
            session['rol'] = user[2]  # Obtener el rol del usuario desde la base de datos
            logged_in_ips[nombre] = obtener_direccion_ip()  # Registrar la IP del usuario

            if user[2] == 'administrador':
                flash('Inicio de sesión exitoso como administrador', 'success')
                return redirect(url_for('inicio'))
            else:
                flash('Inicio de sesión exitoso', 'success')
                return redirect(url_for('inicio'))
        else:
            flash('Nombre de usuario o contraseña incorrectos', 'danger')

    return render_template('index.html')