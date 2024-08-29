

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
        datos_agrupados = []
        total_hojas_por_color_y_producto = {}
        total_hojas_por_seccion = {}
        color_actual = None
        seccion_actual = None

        for producto in data:
            color = producto[2]
            seccion = producto[3]
            nombre = producto[1]
            hojas = producto[7]

            # Agrupación por color y producto
            clave_color_producto = (nombre, color)
            if color_actual is None:
                color_actual = color
            if color != color_actual:
                # Añadir una fila para mostrar el total de hojas para el color anterior
                for (nombre_prod, color_prod), total_hojas in total_hojas_por_color_y_producto.items():
                    total_row = (None, f"Total de hojas de {nombre_prod} color {color_prod}", None, None, None, None, None, total_hojas, None, None)
                    datos_agrupados.append(total_row)
                # Reiniciar el conteo para el nuevo color
                total_hojas_por_color_y_producto = {}
                color_actual = color

            if clave_color_producto not in total_hojas_por_color_y_producto:
                total_hojas_por_color_y_producto[clave_color_producto] = 0
            total_hojas_por_color_y_producto[clave_color_producto] += hojas

            # Agrupación por sección
            if seccion_actual is None:
                seccion_actual = seccion
            if seccion != seccion_actual:
                # Añadir una fila para mostrar el total de hojas para la sección anterior
                total_row = (None, None, f"Total de hojas de la sección {seccion_actual}", None, None, None, None, total_hojas_por_seccion[seccion_actual], None, None)
                datos_agrupados.append(total_row)
                # Reiniciar el conteo para la nueva sección
                seccion_actual = seccion
            if seccion not in total_hojas_por_seccion:
                total_hojas_por_seccion[seccion] = 0
            total_hojas_por_seccion[seccion] += hojas

            datos_agrupados.append(producto)

        # Añadir la última fila de total para el último color y producto
        for (nombre_prod, color_prod), total_hojas in total_hojas_por_color_y_producto.items():
            total_row = (None, f"Total de hojas de {nombre_prod} color {color_prod}", None, None, None, None, None, total_hojas, None, None)
            datos_agrupados.append(total_row)

        if seccion_actual is not None:
            total_row = (None, None, f"Total de hojas de la sección {seccion_actual}", None, None, None, None, total_hojas_por_seccion[seccion_actual], None, None)
            datos_agrupados.append(total_row)
        sql_count = "SELECT COUNT(*) FROM recepcion_eco"
        cursor.execute(sql_count)
        total_rows = cursor.fetchone()[0]  # Obtener la cantidad total de filas

    except Exception as e:
        print(f"Error al obtener los datos de la base de datos: {e}")
    finally:
        cursor.close()
        mydb.close()

    # Pasar datos agrupados a la plantilla
    return render_template('inicio.html', username=session['username'], rol=session['rol'], busqu = data, dato=datos_agrupados, total_rows = total_rows)





@app.route('/filtrar_busqueda', methods=['POST'])
def filtrar_busqueda():
    try:
        name = request.form.get('name')
        color = request.form.get('color')
        client = request.form.get('client')
        session = request.form.get('session')
        tipo_prod = request.form.get('tipo_prod')
        page = int(request.form.get('page', 1))  # Valor por defecto 1 si no se proporciona
        per_page = int(request.form.get('per_page', 10000))  # Valor por defecto 10000

        # Base de la consulta
        query = """
            SELECT tarjeta, nombre, color, seccion, tip_prod, tipo_produccion, fecha, hojas, calibre, cliente
            FROM recepcion_eco
            WHERE 1=1
        """
        filters = []

        # Aplicar filtros según los campos recibidos en el formulario
        if name:
            query += " AND nombre LIKE %s"
            filters.append(f"%{name}%")
        if color:
            query += " AND color LIKE %s"
            filters.append(f"%{color}%")
        if client:
            query += " AND cliente LIKE %s"
            filters.append(f"%{client}%")
        if session:
            query += " AND seccion LIKE %s"
            filters.append(f"%{session}%")
        if tipo_prod:
            query += " AND tip_prod LIKE %s"
            filters.append(f"%{tipo_prod}%")
        
        # Ordenar resultados
        query += """
            ORDER BY 
            FIELD(LEFT(nombre, 1), 'NO', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'A', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z'),
            nombre,
            FIELD(LEFT(color, 1), 'N', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'A', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z'),
            color,
            FIELD(seccion, 'ACABADOS', 'ACONDICIONADO', 'REBAJADO', 'PELAMBRE', 'CURTIDO', 'MATERIAL PRIMA', 'TENIDO'),
            seccion
        """

        # Limitar resultados para paginación
        offset = (page - 1) * per_page
        query += " LIMIT %s OFFSET %s"
        filters.extend([per_page, offset])
        
        # Conexión y ejecución de la consulta
        mydb.connect()
        cursor = mydb.cursor()
        cursor.execute(query, filters)
        results = cursor.fetchall()

        # Procesar los resultados para agregar totales de hojas por color, producto y sección
        datos_agrupados = []
        total_hojas_por_color_y_producto = {}
        total_hojas_por_seccion = {}
        color_actual = None
        seccion_actual = None

        for producto in results:
            color = producto[2]
            seccion = producto[3]
            nombre = producto[1]
            hojas = producto[7]

            # Agrupación por color y producto
            clave_color_producto = (nombre, color)
            if color_actual is None:
                color_actual = color
            if color != color_actual:
                for (nombre_prod, color_prod), total_hojas in total_hojas_por_color_y_producto.items():
                    total_row = (None, f"Total de hojas de {nombre_prod} color {color_prod}", None, None, None, None, None, total_hojas, None, None)
                    datos_agrupados.append(total_row)
                total_hojas_por_color_y_producto = {}
                color_actual = color

            if clave_color_producto not in total_hojas_por_color_y_producto:
                total_hojas_por_color_y_producto[clave_color_producto] = 0
            total_hojas_por_color_y_producto[clave_color_producto] += hojas

            # Agrupación por sección
            if seccion_actual is None:
                seccion_actual = seccion
            if seccion != seccion_actual:
                if seccion_actual in total_hojas_por_seccion:
                    total_row = (None, None, f"Total de hojas de la sección {seccion_actual}", None, None, None, None, total_hojas_por_seccion[seccion_actual], None, None)
                    datos_agrupados.append(total_row)
                seccion_actual = seccion
            if seccion not in total_hojas_por_seccion:
                total_hojas_por_seccion[seccion] = 0
            total_hojas_por_seccion[seccion] += hojas

            datos_agrupados.append(producto)

        # Agregar totales restantes por color y producto
        for (nombre_prod, color_prod), total_hojas in total_hojas_por_color_y_producto.items():
            total_row = (None, f"Total de hojas de {nombre_prod} color {color_prod}", None, None, None, None, None, total_hojas, None, None)
            datos_agrupados.append(total_row)

        # Agregar total restante por sección
        if seccion_actual is not None and seccion_actual in total_hojas_por_seccion:
            total_row = (None, None, f"Total de hojas de la sección {seccion_actual}", None, None, None, None, total_hojas_por_seccion[seccion_actual], None, None)
            datos_agrupados.append(total_row)

        return jsonify({'data': datos_agrupados})

    except Exception as e:
        # Es recomendable no exponer errores detallados en producción
        return jsonify({'error': str(e)}), 500

    finally:
        try:
            cursor.close()
        except:
            pass
        try:
            mydb.close()
        except:
            pass
