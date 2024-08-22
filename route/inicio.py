

from flask import jsonify, request
from app import app, session, render_template
from route.seguridad import login_required
from conexion import mydb


@app.route('/inicio')
@login_required
def inicio():
    data = []
    try:
        # Conectar a la base de datos
        mydb.connect()
        cursor = mydb.cursor()

        # Consultar datos de la base de datos
        sql = """
            SELECT tarjeta, nombre, color, seccion, tip_prod, tipo_produccion, fecha, hojas, calibre, cliente
            FROM recepcion_eco
            ORDER BY FIELD(LEFT(seccion, 1), 'A',  'R', 'P', 'C', 'M', 'T'),
            seccion,
            FIELD(LEFT(nombre, 1), 'N', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'A', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z'),
            nombre,
            FIELD(LEFT(color, 1), 'N', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'A', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z' ),
            color;   
        """

        cursor.execute(sql)
        data = cursor.fetchall()    

        # Agrupar productos por color y calcular el total de hojas
        datos_agrupado2 = []
        datos_agrupados = []
        total_hojas_por_color = {}
        color_actual = None
        seccion_actual = None
        total_hojas_por_seccion = {}

        for producto in data:
            color = producto[2]
            hojas = producto[7]

            if color_actual is None:
                color_actual = color

            if color != color_actual:
                # Añadir una fila para mostrar el total de hojas para el color anterior
                total_row = (None, None, color_actual, None, None, None, None, total_hojas_por_color[color_actual], None, None)
                datos_agrupados.append(total_row)
                
                # Reiniciar el conteo para el nuevo color
                color_actual = color

            if color not in total_hojas_por_color:
                total_hojas_por_color[color] = 0
            total_hojas_por_color[color] += hojas

            datos_agrupados.append(producto)

        #Sarcar cantdad de hojas que hay por sesion
        for datos in data:
            seccion = datos[3]
            hoja = datos[7]
            if seccion_actual is None:
                sesion_actual = seccion

            if seccion != sesion_actual:
                # Añadir una fila para mostrar el total de hojas para la sesion anterior
                total_row = (None, None, None, sesion_actual, None, None, None, total_hojas_por_seccion[sesion_actual], None, None)
                datos_agrupados.append(total_row)

                sesion_actual =seccion

            if seccion not in total_hojas_por_seccion:
                total_hojas_por_seccion[seccion] = 0
            total_hojas_por_seccion[seccion] += hoja

            datos_agrupado2.append(datos)


        # Añadir la última fila de total para el último color
        if color_actual is not None:
            total_row = (None, None, color_actual, None, None, None, None, total_hojas_por_color[color_actual], None, None)
            datos_agrupados.append(total_row)

        if seccion_actual is not None:
            total_row = (None, None, None, seccion_actual, None, None, None, total_hojas_por_seccion[seccion_actual], None, None)
            datos_agrupado2.append(total_row)

    except Exception as e:
        print(f"Error al obtener los datos de la base de datos: {e}")
    finally:
        cursor.close()
        mydb.close()

    # Pasar datos agrupados a la plantilla
    return render_template('inicio.html', username=session['username'], rol=session['rol'], dato=datos_agrupados, dato2 = datos_agrupado2)





@app.route('/filtrar_busqueda', methods=['POST'])
def filtrar_busqueda():
    name = request.form.get('name')
    color = request.form.get('color')
    caliber = request.form.get('caliber')
    client = request.form.get('client')
    session = request.form.get('session')
    tipo_prod = request.form.get('tipo_prod')
    page = int(request.form.get('page'))
    per_page = int(request.form.get('per_page'))
    
    query = """
        SELECT tarjeta, nombre, color, seccion, tip_prod, tipo_produccion, fecha, hojas, calibre, cliente
        FROM recepcion_eco 
        WHERE 1=1
        
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
        mydb.connect()
        cursor = mydb.cursor()
        cursor.execute(query, filters)
        results = cursor.fetchall()

        cursor.execute("""
        SELECT COUNT(*) FROM recepcion_eco WHERE 1=1
        ORDER BY FIELD(LEFT(nombre, 1), 'N', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'A', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z'),
        nombre,
        FIELD(LEFT(color, 1), 'N', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'A', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z' ),
        color;""")
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