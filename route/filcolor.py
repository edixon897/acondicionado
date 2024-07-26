from conexion import mydb
from app import flash, request, render_template, url_for, app, session



@app.route('filtro_colores')
def filtro_colores():
    try:
        mycursor = mydb.cursor()
        mycursor.execute("SELECT   `color`, `seccion`, `hojas` FROM `recepcion_eco`")
        myresult = mycursor.fetchall()

    except Exception as e:
        print(f"Error al obtener los datos de la base de datos: {e}")
    finally:
        mycursor.close()
        mydb.close()
    return render_template('resumen.html',  username=session['username'], rol = session['rol'], colores=myresult)