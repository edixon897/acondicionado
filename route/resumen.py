
from app import app, render_template, session
from route.seguridad import login_required
from conexion import mydb


@app.route('/resumen')
@login_required
def resumen():
    try:
        mydb.connect()
        cursor = mydb.cursor()

        # Aggregating hojas by color and seccion
        sql = """
            SELECT color, seccion, SUM(hojas) AS total_hojas
            FROM recepcion_eco
            GROUP BY color, seccion
            ORDER BY color DESC, seccion
        """

        cursor.execute(sql)
        data = cursor.fetchall()

    except Exception as e:
        print(f"Error al obtener los datos de la base de datos: {e}")
    finally:
        mydb.close()

    # Pass the aggregated data to the template
    return render_template('resumen.html', username=session['username'], rol=session['rol'], colores=data)