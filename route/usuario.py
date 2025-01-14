from flask import jsonify
from app import app, request, flash, redirect, session,  render_template, url_for
from route.seguridad import login_required
from conexion import create_connection, close_connection

@app.route('/agregarUsuario', methods=['GET', 'POST'])
@login_required
def agregarUsuario():
    connection = create_connection()
    if connection is None:
        
        return None
    try:
        if request.method == 'POST':
            nombre = request.form.get('nombre_usuario').capitalize()
            apellido = request.form.get('apellido').capitalize()
            contraseña = request.form.get('contrasena')
            repetir_nueva_contraseña = request.form.get('contrasena2')

            if contraseña != repetir_nueva_contraseña:
                return jsonify({'message': 'Algo salio mal al registrar por favor vuelva a intentarlo'})


            
            cursor = connection.cursor()
            cursor.execute(f"""INSERT INTO `usuario`(`nombre`, `apellido`, `contrasena`, `rol`, `estado`) 
                           VALUES  ('{nombre}', '{apellido}','{contraseña}', 'usuario', 'Activo')""")
            connection.commit()
            cursor.close()
            connection.close()
            
            flash('Usuario registrado exitosamente', 'success')

            return jsonify({"succes": True,"message": "!Usuario Registrado con exito¡", "redirect_url": url_for('agregarUsuario')})

        
    except Exception as e:
       
        return None
    
    finally:
        close_connection(connection)    

    return render_template('agregar_usuario.html', username=session.get('username'), rol=session.get('rol'))

