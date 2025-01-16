from flask import jsonify
from app import app, session, flash, redirect, url_for, request,  render_template, logged_in_ips
from route.seguridad import login_required, obtener_direccion_ip

from conexion import create_connection, close_connection



@app.route('/logout')
@login_required
def logout():
    if 'username' in session:
        # Elimina la entrada del usuario de sesiones activas
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
        return None
    try:
        if request.method == 'POST':
            nombre = request.form.get('nombre').capitalize()
            contraseña = request.form.get('contraseña')
            destino = request.form.get('destino')
            
            
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
                session['destino'] = destino

                logged_in_ips[nombre] = obtener_direccion_ip()  
                

                if user[2] == 'administrador' and user[3] == 'Activo':
                    if destino == 'produccion':
                        flash('Inicio de sesión en Producción exitoso', 'success')
                        return jsonify({"success": True, "message": "Inicio de sesión en Producción exitoso", "redirect_url": url_for('inicio')})
                    
                    elif destino == 'almacen':
                        flash('Inicio de sesión en Almacén exitoso', 'success')
                        return jsonify({"success": True, "message": "Inicio de sesión en Almacén exitoso", "redirect_url": url_for('inicio_almacen')})
                    
                    else:
                        return jsonify({"success": False, "error": "Destino inválido."})
                    
                elif user[2] == 'usuario' and user[3] == 'Activo':

                    if destino == 'produccion':
                        flash('Inicio de sesión en Producción exitoso', 'success')
                        return jsonify({"success": True, "message": "Inicio de sesión en Producción exitoso", "redirect_url": url_for('inicio')})
                    
                    elif destino == 'almacen':
                        print('sesion en almacen')
                        flash('Inicio de sesión en Almacén exitoso', 'success')
                        return jsonify({"success": True, "message": "Inicio de sesión en Almacén exitoso", "redirect_url": url_for('inicio_almacen')})
                    
                    else:
                        return jsonify({"success": False, "error": "Destino inválido."})     
                
                else:
                    return jsonify({"success": False, "message": "Tu usuario no esta activo, comunicate con aministracion"})
                    
                    
            else:
                return jsonify({"success": False, "error": "Nombre de usuario o contraseña incorrectos."})
            
    except Exception as e:
        
        return None
    
    finally:
        close_connection(connection)       

    return render_template('index.html')