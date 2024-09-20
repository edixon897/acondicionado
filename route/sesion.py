from flask import jsonify
from app import app, session, flash, redirect, url_for, request,  check_password_hash, render_template, logged_in_ips
from route.seguridad import login_required, obtener_direccion_ip

from conexion import create_connection, close_connection



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
    connection = create_connection()
    if connection is None:
        print("No hay conexión con la base de datos")
        return None
    try:
        if request.method == 'POST':
            nombre = request.form.get('nombre')
            contraseña = request.form.get('contraseña')

            
            cursor = connection.cursor()

            cursor.execute("SELECT nombre, contrasena, rol, estado FROM usuario WHERE nombre = %s AND contrasena = %s AND estado = %s", (nombre, contraseña, 'Activo'))
            user = cursor.fetchone()
            cursor.close()
            connection.close()

            if user:
                session['logged_in'] = True
                session['username'] = nombre
                session['rol'] = user[2]
                session['estado'] = user[3]

                logged_in_ips[nombre] = obtener_direccion_ip()  

                if user[2] == 'administrador':
                    flash('Inicio de sesión exitoso como administrador', 'success')
                    return jsonify({"success": True, "message": "Inicio de sesión exitoso como administrador", "redirect_url": url_for('inicio')})
                elif user[3] == 'Inactivo':
                    return jsonify({"success": False, "message": "Tu usuario no esta activo, comunicate con aministracion"})
                else:       
                    flash('Inicio de sesión exitoso', 'success')
                    return jsonify({"success": True, "message": "Inicio de sesión exitoso", "redirect_url": url_for('inicio')})
            else:
                return jsonify({"success": False, "error": "Nombre de usuario o contraseña incorrectos."})
            
    except Exception as e:
        print(f"Error al consultar usuarios: {e}")
        return None
    
    finally:
        close_connection(connection)       

    return render_template('index.html')