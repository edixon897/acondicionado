

from flask import jsonify, request
from app import app, session, render_template
from route.seguridad import login_required
from conexion import mydb



@app.route('/inicio')
@login_required
def inicio():
    data = []
    try:
        mydb.connect()
        cursor = mydb.cursor()
        
      

        sql = f"""
            SELECT tarjeta, nombre, color, seccion, tip_prod, familia, fecha, hojas, calibre, cliente
            FROM recepcion_eco
            ORDER BY `color` DESC
        """

        cursor.execute(sql)
        data = cursor.fetchall()
        print('datos mysql:  ',   data)

    except Exception as e:
        print(f"Error al obtener los datos de la base de datos: {e}")
    finally:
        cursor.close()
        mydb.close()

    return render_template('inicio.html', username=session['username'], rol=session['rol'], dato=data)





@app.route('/filtrar_busqueda', methods=['POST'])
def filtrar_busqueda():
    name = request.form.get('name')
    color = request.form.get('color')
    caliber = request.form.get('caliber')
    client = request.form.get('client')
    session = request.form.get('session')
    tipo_prod = request.form.get('tipo_prod')
    page = int(request.form.get('page', 1))
    per_page = int(request.form.get('per_page', 10))
    
    query = """
        SELECT tarjeta, nombre, color, seccion, tip_prod, familia, fecha, hojas, calibre, cliente
        FROM recepcion_eco WHERE 1=1
    """
    filters = []
    
    if name:
        query += " AND nombre LIKE %s"
        filters.append(f"%{name}%")
    if color:
        query += " AND color LIKE %s"
        filters.append(f"%{color}%")
    if caliber:
        query += " AND calibre LIKE %s"
        filters.append(f"%{caliber}%")
    if client:
        query += " AND cliente LIKE %s"
        filters.append(f"%{client}%")
    if session:
        query += " AND seccion LIKE %s"
        filters.append(f"%{session}%")
    if tipo_prod:
        query += " AND tip_prod LIKE %s"
        filters.append(f"%{tipo_prod}%")
    
    offset = (page - 1) * per_page
    query += " LIMIT %s OFFSET %s"
    filters.extend([per_page, offset])
    
    try:
        conn = mydb.connect()
        cursor = mydb.cursor()
        cursor.execute(query, filters)
        results = cursor.fetchall()

        cursor.execute("SELECT COUNT(*) FROM recepcion_eco WHERE 1=1")
        total_count = cursor.fetchone()[0]

        return jsonify({
            'data': results,
            'total_count': total_count
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        cursor.close()
        mydb.close()