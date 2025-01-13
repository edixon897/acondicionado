from app import request,functools, session, logged_in_ips, flash, redirect, url_for, app



# Funcion para obtener la dirección IP del cliente
def obtener_direccion_ip():
    if 'X-Forwarded-For' in request.headers:
        return request.headers.getlist('X-Forwarded-For')[0]
    else:
        return request.remote_addr

# Funcion para requerir inicio de sesion
def login_required(f):
    @functools.wraps(f)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
            # Agregar la dirección IP a la lista si no está presente
            ip_address = obtener_direccion_ip()
            if session['username'] not in logged_in_ips:
                logged_in_ips[session['username']] = ip_address
            return f(*args, **kwargs)
        else:
            flash('Necesitas iniciar sesión primero.', 'danger')
            return redirect(url_for('login'))
    return wrap





