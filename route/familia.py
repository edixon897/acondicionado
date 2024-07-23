from app import app, redirect, session, render_template

from route.seguridad import login_required

@app.route('/familia')
@login_required
def familia():
    return render_template('familia.html', username=session['username'], rol = session['rol'])