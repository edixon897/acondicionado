
from app import app, render_template, session, request, jsonify
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
@app.route('/buscar_color')
def buscar_color():
    try:
        mydb.connect()
        cursor = mydb.cursor()
        color = request.args.get('color')
        sql = """
        SELECT color, seccion, SUM(hojas) AS total_hojas
        FROM recepcion_eco
        WHERE color LIKE %s
        GROUP BY color, seccion
        ORDER BY seccion
        """
        cursor.execute(sql, ('%' + color + '%',))
        data = cursor.fetchall()

        suggestions = [row[0] for row in data]
        results = [{'color': row[0], 'seccion': row[1], 'total_hojas': row[2]} for row in data]
        
        response = {
            'suggestions': list(set(suggestions)),
            'results': results
        }
        return jsonify(response)

    except Exception as e:
        print(f"Error al obtener los datos de la base de datos: {e}")
        return jsonify({'error': str(e)})

    finally:
        mydb.close()