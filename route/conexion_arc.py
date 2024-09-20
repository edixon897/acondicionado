import time
import pandas as pd
import mysql.connector
import os
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from conexion import create_connection



# Nombres de columnas del archivo .prn
column_names = ['tarjeta', 'tip_prod', 'nombre', 'color', 'calibre', 'seccion', 'tipo_produccion', 'hojas', 'cliente', 'fecha']

# Función para limpiar valores NaN, espacios sin datos
def clean_data(df):
    print("Limpiando datos NaN...")
    df = df.fillna('')  # Se remplaza por para que registre una cadena vacia
    print("Datos limpiados:")
    print(df.head())
    return df

# Función para verificar si el registro ya existe en la base de datos
def is_duplicate(cursor, row):
    query = """SELECT COUNT(*) FROM `recepcion_eco` WHERE `tarjeta` = %s AND `tip_prod` = %s AND `nombre` = %s 
               AND `color` = %s AND `calibre` = %s AND `seccion` = %s AND `tipo_produccion` = %s AND `hojas` = %s 
               AND `cliente` = %s AND `fecha` = %s"""
    cursor.execute(query, tuple(row))
    count = cursor.fetchone()[0]
    if count > 0:
        print(f"Registro duplicado encontrado: {row}")
    else:
        print(f"Registro único: {row}")
    return count > 0

# Función para insertar datos en la base de datos
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
            print(f"Procesando lote {start // batch_size + 1}:")
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
                    time.sleep(1)  # Espera antes de insertar el siguiente registro
                else:
                    print(f"Registro duplicado. Esperando nuevos datos...")
                         
        cursor.close()
        print("Inserción de datos completada.")
    except mysql.connector.Error as err:
        print(f"Error al insertar datos en la base de datos: {err}")
    except Exception as e:
        print(f"Error inesperado: {e}")

# Función para leer el archivo y procesar datos que se encuentran en el archivo
def process_file(file_path):
    print(f"Procesando el archivo: {file_path}")
    try:
        df = pd.read_csv(file_path, sep=',', header=None, names=column_names, skipinitialspace=True)
        print("Archivo leído con éxito:")
        print(df.head())
        df = clean_data(df)
        insert_data(df)
    except Exception as e:
        print(f"Error al procesar el archivo: {e}")

# Clase que personaliza Handler para Watchdog 
class WatcherHandler(FileSystemEventHandler):
    def on_modified(self, event):
        if event.src_path == file_path:
            print(f"Archivo modificado detectado: {event.src_path}")
            process_file(event.src_path)

# Ruta del archivo a monitorear
file_path = r'\\192.168.0.114\D\compartidos\plsaldo.prn'

# Función principal que vigila, verifica y registra continuamente y automaticamente
def monitor_and_process():
    # Verificar si el archivo existe antes de iniciar la vigilancia
    if not os.path.exists(file_path):
        print(f"El archivo {file_path} no existe.")
        return

    print(f"Vigilando el archivo: {file_path}")
    event_handler = WatcherHandler()
    observer = Observer()
    observer.schedule(event_handler, path=os.path.dirname(file_path), recursive=False)
    observer.start()

    try:
        while True:
            process_file(file_path)  # Verificar y registrar cada ciclo
            print("Esperando 10 segundos antes de la siguiente verificación...")
            time.sleep(10)  # Intervalo de espera antes de la siguiente verificación
    except KeyboardInterrupt:
        observer.stop()
    observer.join()
    print("Vigilancia finalizada.")

# Iniciar la función principal
monitor_and_process()
