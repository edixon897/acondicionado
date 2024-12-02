from flask import jsonify, request
from app import app, session, render_template
from route.seguridad import login_required
from conexion import create_connection, close_connection

from route.seguridad import login_required

@app.route('/familia')
@login_required
def familia():
    return render_template('familia.html', username=session['username'], rol = session['rol'])



def buscar_producto(nombre_producto):
    connection = create_connection()
    if connection is None:
        
        return None
    try:
        cursor = connection.cursor()
        
        query = "SELECT tarjeta, nombre, color, seccion, tip_prod, tipo_produccion, fecha, hojas, calibre, cliente FROM recepcion_eco WHERE tarjeta LIKE %s"
        cursor.execute(query, ('%' + nombre_producto + '%',))
        
        resultados = cursor.fetchall()
        cursor.close()

        productos = []
        for row in resultados:
            productos.append({
                'tarjeta': row[0],
                'nombre': row[1],
                'color': row[2],
                'seccion': row[3],
                'tip_prod': row[4],
                'tipo_produccion': row[5],
                'fecha': row[6],
                'hojas': row[7],
                'calibre': row[8],
                'cliente': row[9]

                
            })

        return productos
    
    except Exception as e:
        
        return None
    
    finally:
        close_connection(connection)

@app.route('/buscar', methods=['GET'])
def buscar():
    nombre_producto = request.args.get('nombre')
    resultados = buscar_producto(nombre_producto)
    return jsonify(resultados)


