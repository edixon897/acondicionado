
from app import app, render_template, session
from route.seguridad import login_required


@app.route('/resumen')
@login_required
def resumen():
    return render_template('resumen.html', username=session['username'], rol = session['rol'])