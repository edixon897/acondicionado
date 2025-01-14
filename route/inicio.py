


from app import app, session, render_template, jsonify, request
from route.seguridad import login_required
from conexion import create_connection, close_connection


@app.route('/inicio')
@login_required
def inicio():
    data = []
    try:
        connection = create_connection()
        if connection is None:
            
            return None

        cursor = connection.cursor()

        
        sql = """
            SELECT tarjeta, nombre, color, seccion, tip_prod, tipo_produccion, fecha, hojas, calibre, cliente
            FROM recepcion_eco WHERE 20
            ORDER BY FIELD(LEFT(seccion, 1), 'A',  'R', 'P', 'C', 'M', 'T'),
            seccion,
            FIELD(LEFT(nombre, 1), 'N', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'A', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z'),
            nombre,
            FIELD(LEFT(color, 1), 'N', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'A', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z' ),
            color
            
        """

        cursor.execute(sql)
        data = cursor.fetchall()

        datos_agrupados = []
        total_hojas_por_nombre_color = {}
        total_hojas_por_color = {}
        total_hojas_por_nombre = {}
        total_hojas_por_seccion = {}
        seccion_actual, color_actual, nombre_actual = None, None, None

        for producto in data:
            tarjeta, nombre, color, seccion, tip_prod, tipo_produccion, fecha, hojas, calibre, cliente = producto
           

            # Agrupacion por color dentro de la sección
            if color != color_actual:
                if color_actual is not None:
                    #fila de total por color
                    datos_agrupados.append((None, None, f"Total de hojas {nombre_actual} color {color_actual}", None, None, None, None, total_hojas_por_color[color_actual], None, None))
                color_actual = color
                total_hojas_por_color[color] = 0

            total_hojas_por_color[color] += hojas

            # Agrupacion por nombre dentro de la seccion
            if nombre != nombre_actual:
                if nombre_actual is not None:
                    #fila de total por nombre
                    datos_agrupados.append((None, f"Total de hojas de {nombre_actual}", None, None, None, None, None, total_hojas_por_nombre[nombre_actual], None, None))
                nombre_actual = nombre
                total_hojas_por_nombre[nombre] = 0

            if seccion != seccion_actual:
                if seccion_actual is not None:
                    #fila de total por sección
                    datos_agrupados.append((None, None, None, f"Total de hojas de la sección {seccion_actual}", None, None, None, total_hojas_por_seccion[seccion_actual], None, None))
                seccion_actual = seccion
                total_hojas_por_seccion[seccion] = 0

            total_hojas_por_seccion[seccion] += hojas

            total_hojas_por_nombre[nombre] += hojas

            # Agrupacion por nombre y color
            clave_nombre_color = (nombre, color)
            if clave_nombre_color not in total_hojas_por_nombre_color:
                total_hojas_por_nombre_color[clave_nombre_color] = 0
            total_hojas_por_nombre_color[clave_nombre_color] += hojas

           
            datos_agrupados.append(producto)

        # Añadir los ultimos totales pendientes
        
        if color_actual:
            datos_agrupados.append((None, None, f"Total de hojas color {color_actual}", None, None, None, None, total_hojas_por_color[color_actual], None, None))
        if nombre_actual:
            datos_agrupados.append((None, f"Total de hojas de {nombre_actual}", None, None, None, None, None, total_hojas_por_nombre[nombre_actual], None, None))
        if seccion_actual:
            datos_agrupados.append((None, None, None, f"Total de hojas de la sección {seccion_actual}", None, None, None, total_hojas_por_seccion[seccion_actual], None, None))

        # Añadir los totales por nombre y color
        #for (nombre, color), total_hojas in total_hojas_por_nombre_color.items():
         #   datos_agrupados.append((None, f"Total de hojas de {nombre} color {color}", None, None, None, None, None, total_hojas, None, None))



    except Exception as e:
        
        return None
    
    finally:
        close_connection(connection)


    return render_template('inicio.html', username=session['username'], rol=session['rol'], busqu=data, dato=datos_agrupados)


@app.route('/produc_filtrar', methods=['GET'])
def produc_filtrar():
    data = []
    try:
        connection = create_connection()
        if connection is None:
            
            return None

        cursor = connection.cursor()

        
        sql = """
            SELECT tarjeta, nombre, color, seccion, tip_prod, tipo_produccion, fecha, hojas, calibre, cliente
            FROM recepcion_eco WHERE 20
            ORDER BY FIELD(LEFT(seccion, 1), 'A',  'R', 'P', 'C', 'M', 'T'),
            seccion,
            FIELD(LEFT(nombre, 1), 'N', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'A', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z'),
            nombre,
            FIELD(LEFT(color, 1), 'N', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'A', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z' ),
            color
            LIMIT 100;
        """

        cursor.execute(sql)
        data = cursor.fetchall()

    except Exception as e:
        
        return None
    
    finally:
        close_connection(connection)




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
        if client:
            query += " AND cliente LIKE %s"
            filters.append(f"%{client}%")
        if session:
            query += " AND seccion LIKE %s"
            filters.append(f"%{session}%")
        if tipo_prod:
            query += " AND tipo_produccion LIKE %s"
            filters.append(f"%{tipo_prod}%")
        
        query += """
            ORDER BY FIELD(LEFT(seccion, 1), 'A',  'R', 'P', 'C', 'M', 'T'),
            seccion,
            FIELD(LEFT(nombre, 1), 'N', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'A', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z'),
            nombre,
            FIELD(LEFT(color, 1), 'N', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'A', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z' ),
            color
        """

        # Limitar resultados para paginacion
        offset = (page - 1) * per_page
        query += " LIMIT %s OFFSET %s"
        filters.extend([per_page, offset])
        
        connection = create_connection()
        if connection is None:
            
            return None
        cursor = connection.cursor()
        cursor.execute(query, filters)
        results = cursor.fetchall()

        # Procesar los resultados para agregar totales de hojas por color, producto y sección
        datos_agrupados = []
        total_hojas_por_nombre_color = {}
        total_hojas_por_color = {}
        total_hojas_por_nombre = {}
        total_hojas_por_seccion = {}
        seccion_actual, color_actual, nombre_actual = None, None, None

        for producto in results:
            tarjeta, nombre, color, seccion, tip_prod, tipo_produccion, fecha, hojas, calibre, cliente = producto

            

            # Agrupacion por color dentro de la seccion
            if color != color_actual:
                if color_actual is not None:
                    #fila de total por color
                    datos_agrupados.append((None, None, f"Total de hojas {nombre_actual} color {color_actual}", None, None, None, None, total_hojas_por_color[color_actual], None, None))
                color_actual = color
                total_hojas_por_color[color] = 0

            total_hojas_por_color[color] += hojas

            # Agrupacion por nombre dentro de la seccion
            if nombre != nombre_actual:
                if nombre_actual is not None:
                    #fila de total por nombre
                    datos_agrupados.append((None, f"Total de hojas de {nombre_actual}", None, None, None, None, None, total_hojas_por_nombre[nombre_actual], None, None))
                nombre_actual = nombre
                total_hojas_por_nombre[nombre] = 0

            total_hojas_por_nombre[nombre] += hojas

            if seccion != seccion_actual:
                if seccion_actual is not None:
                    # Añadir fila de total por seccion
                    datos_agrupados.append((None, None, None, f"Total de hojas de la sección {seccion_actual}", None, None, None, total_hojas_por_seccion[seccion_actual], None, None))
                seccion_actual = seccion
                total_hojas_por_seccion[seccion] = 0

            total_hojas_por_seccion[seccion] += hojas

            # Agrupacion por nombre y color
            clave_nombre_color = (nombre, color)
            if clave_nombre_color not in total_hojas_por_nombre_color:
                total_hojas_por_nombre_color[clave_nombre_color] = 0
            total_hojas_por_nombre_color[clave_nombre_color] += hojas

            # Añadir el producto al grupo
            datos_agrupados.append(producto)

        #los últimos totales pendientes
       
        if color_actual:
            datos_agrupados.append((None, None, f"Total de hojas color {color_actual}", None, None, None, None, total_hojas_por_color[color_actual], None, None  ))
        if nombre_actual:
            datos_agrupados.append((None, f"Total de hojas de {nombre_actual}", None, None, None, None, None,total_hojas_por_nombre[nombre_actual],  None, None ))
        if seccion_actual:
            datos_agrupados.append((None, None, None, f"Total de hojas de la sección {seccion_actual}", None, None, None, total_hojas_por_seccion[seccion_actual],  None, None ))

        # los totales por nombre y color
        #for (nombre, color), total_hojas in total_hojas_por_nombre_color.items():
         #   datos_agrupados.append((None, f"Total de hojas de {nombre} color {color}", None, None, None, None, None, total_hojas, None, None))

        return jsonify({'data': datos_agrupados}) 

    except Exception as e:
        return jsonify({'error': str(e)}), 500

    
    finally:
        close_connection(connection)
