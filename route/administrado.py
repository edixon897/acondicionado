import sqlite3
from flask import flash
from app import render_template, session, app, logged_in_ips, redirect, url_for

from route.seguridad import login_required


# Ruta para la página de administrador
@app.route('/administrador', methods=['GET'])
@login_required
def administrador():
    # Asegurarse de que el usuario sea administrador para acceder a esta página
    if session['rol'] != 'administrador':
        flash('Acceso no autorizado', 'danger')
        return redirect(url_for('inicio'))

    # Obtener todos los usuarios de la base de datos
    conn = sqlite3.connect('usuario.db')
    c = conn.cursor()
    c.execute('SELECT * FROM users')
    usuarios = c.fetchall()
    conn.close()

    # Construir lista de sesiones activas y estado de cada usuario
    sesiones_activas = []

    for usuario in usuarios:
        username = usuario[1]
        estado = 'Activo' if username in logged_in_ips else 'Inactivo'
        sesiones_activas.append({
            'username': username,
            'ip_address': logged_in_ips.get(username, 'No disponible'),
            'estado': estado
        })

    return render_template('administrador.html', sesiones_activas=sesiones_activas)


@app.route('/actualizar_sesiones_activas', methods=['GET'])
@login_required
def actualizar_sesiones_activas():
    # Obtener todos los usuarios de la base de datos
    conn = sqlite3.connect('usuario.db')
    c = conn.cursor()
    c.execute('SELECT * FROM users')
    usuarios = c.fetchall()
    conn.close()

    # Construir lista de sesiones activas y estado de cada usuario
    sesiones_activas = []

    for usuario in usuarios:
        username = usuario[1]
        estado = 'Activo' if username in logged_in_ips else 'Inactivo'
        sesiones_activas.append({
            'username': username,
            'ip_address': logged_in_ips.get(username, 'No disponible'),
            'estado': estado
        })

    return render_template('_sesiones_activas.html', sesiones_activas=sesiones_activas)



