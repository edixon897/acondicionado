import time
import pandas as pd
import mysql.connector
import os
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from conexion import create_connection
import threading



# Nombres de columnas del archivo .prn
column_names = ['tarjeta', 'tip_prod', 'nombre', 'color', 'calibre', 'seccion', 'tipo_produccion', 'hojas', 'cliente', 'fecha']

# Funcion para limpiar valores NaN, espacios sin datos
def clean_data(df):

    df = df.fillna('')  # Se remplaza para que registre una cadena vacia
    
    return df

# Funcion para verificar si el registro ya existe en la base de datos
def is_duplicate(cursor, row):
    query = """SELECT COUNT(*) FROM `recepcion_eco` WHERE `tarjeta` = %s AND `tip_prod` = %s AND `nombre` = %s 
               AND `color` = %s AND `calibre` = %s AND `seccion` = %s AND `tipo_produccion` = %s AND `hojas` = %s 
               AND `cliente` = %s AND `fecha` = %s"""
    cursor.execute(query, tuple(row))
    count = cursor.fetchone()[0]
    

# Función para insertar datos 
def insert_data(df, batch_size=100):
    try:
        connection = create_connection()
        if connection is None:
            print("No hay conexión con la base de datos")
            return None
        cursor = connection.cursor()
        total_rows = len(df)
        print(f"Total de filas a insertar: {total_rows}")
        for start in range(0, total_rows, batch_size):
            end = start + batch_size
            batch = df.iloc[start:end]

            values = [
                (row['tarjeta'], row['tip_prod'], row['nombre'], row['color'], row['calibre'], row['seccion'],
                    row['tipo_produccion'], row['hojas'], row['cliente'], row['fecha'] if row['fecha'] != '' else None)
                for index, row in batch.iterrows()
            ]
            for value in values:
                if not is_duplicate(cursor, value):
                    sql = """INSERT INTO `recepcion_eco` (`tarjeta`, `tip_prod`, `nombre`, `color`, `calibre`, `seccion`, 
                              `tipo_produccion`, `hojas`, `cliente`, `fecha`)
                              VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"""
                    cursor.execute(sql, value)
                    connection.commit()
                    print(f"Registro insertado con éxito: {value}")
                    time.sleep(1)  # Espera 1 segundo antes de insertar el siguiente registro
                else:
                    print(f"Registro duplicado. Esperando nuevos datos...")
                         
        cursor.close()
        print("Inserción de datos completada.")
    except mysql.connector.Error as err:
        print(f"Error al insertar datos en la base de datos: {err}")
    except Exception as e:
        print(f"Error inesperado: {e}")

# Funcion para leer el archivo y procesar datos que se encuentran en el archivo
def process_file(file_path):
    print(f"Procesando el archivo: {file_path}")
    try:
        df = pd.read_csv(file_path, sep=',', header=None, names=column_names, skipinitialspace=True)
        
        df = clean_data(df)
        insert_data(df)
    except Exception as e:
        print(f"Error al procesar el archivo: {e}")

# Clase que personaliza Handler para Watchdog 
class WatcherHandler(FileSystemEventHandler):
    def on_modified(self, event):
        if event.src_path == file_path:
            process_file(event.src_path)

# Ruta del archivo 
file_path = r'\\192.168.0.114\D\compartidos\plsaldo.prn'

# Función principal que vigila, verifica y registra continuamente y automaticamente, los datos del archivo
def monitor_and_process():
    # Verificar si el archivo existe antes de iniciar la vigilancia, es importaten para que no tengamos error al leer un archivo
    if not os.path.exists(file_path):
        return

    print(f"Vigilando el archivo: {file_path}")
    event_handler = WatcherHandler()
    observer = Observer()
    observer.schedule(event_handler, path=os.path.dirname(file_path), recursive=False)
    observer.start()

    try:
        while True:
            process_file(file_path)  # Verifica y registrar 
            print("Esperando 10 minutos antes de la siguiente verificación...")
            time.sleep(1000)  
    except KeyboardInterrupt:
        observer.stop()
    observer.join()
    print("Vigilancia finalizada.")


# Inicia la ejecución del scheduler en un hilo separado
scheduler_thread = threading.Thread(target=monitor_and_process)
scheduler_thread.daemon = True  # Aseguro que el hilo se cierre cuando la aplicación principal termine
scheduler_thread.start()