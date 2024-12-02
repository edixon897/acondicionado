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

# Función para limpiar valores NaN, espacios sin datos
def clean_data(df):
    df = df.fillna('')  # Se reemplaza para que registre una cadena vacía
    return df

# Función para eliminar y recrear la tabla
def reset_table():
    try:
        connection = create_connection()
        if connection is None:
            return False
        cursor = connection.cursor()
        cursor.execute("DROP TABLE IF EXISTS `recepcion_eco`")
        cursor.execute("""
            CREATE TABLE `recepcion_eco` (
                `tarjeta` VARCHAR(50),
                `tip_prod` VARCHAR(50),
                `nombre` VARCHAR(100),
                `color` VARCHAR(50),
                `calibre` VARCHAR(50),
                `seccion` VARCHAR(50),
                `tipo_produccion` VARCHAR(50),
                `hojas` INT,
                `cliente` VARCHAR(100),
                `fecha` DATE
            )
        """)
        connection.commit()
        cursor.close()
        return True
    except mysql.connector.Error as err:
        return False
    except Exception as e:
        return False

# Función para insertar datos
def insert_data(df, batch_size=100):
    try:
        connection = create_connection()
        if connection is None:
            return False
        cursor = connection.cursor()
        total_rows = len(df)
        for start in range(0, total_rows, batch_size):
            end = start + batch_size
            batch = df.iloc[start:end]
            values = [
                (row['tarjeta'], row['tip_prod'], row['nombre'], row['color'], row['calibre'], row['seccion'],
                 row['tipo_produccion'], row['hojas'], row['cliente'], row['fecha'] if row['fecha'] != '' else None)
                for _, row in batch.iterrows()
            ]
            sql = """INSERT INTO `recepcion_eco` (`tarjeta`, `tip_prod`, `nombre`, `color`, `calibre`, `seccion`, 
                     `tipo_produccion`, `hojas`, `cliente`, `fecha`)
                     VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"""
            cursor.executemany(sql, values)
            connection.commit()
            return True
        cursor.close()
        
    except mysql.connector.Error as err:
        return False
    except Exception as e:
        return False

# Funcion para leer el archivo y procesar datos
def process_file(file_path):

    try:
        df = pd.read_csv(file_path, sep=',', header=None, names=column_names, skipinitialspace=True)
        df = clean_data(df)
        reset_table()  # LLamo la funcion para eliminar y reacrear la tabla recepcion_eco
        insert_data(df)
    except Exception as e:
        return False

# Clase para Watchdog
class WatcherHandler(FileSystemEventHandler):
    def on_modified(self, event):
        if event.src_path == file_path:
            process_file(event.src_path)

# Ruta del archivo a leer
file_path = r'\\192.168.0.114\D\compartidos\plsaldo.prn'

# Función principal que vigila y procesa el archivo automáticamente
def monitor_and_process():
    # Verificar si el archivo existe antes de iniciar la vigilancia
    if not os.path.exists(file_path):
        return False


    event_handler = WatcherHandler()
    observer = Observer()
    observer.schedule(event_handler, path=os.path.dirname(file_path), recursive=False)
    observer.start()

    try:
        while True:
            process_file(file_path)  # Procesa y registra los datos
            time.sleep(600)  # 10 minutos
    except KeyboardInterrupt:
        observer.stop()
    observer.join()

# Inicia la ejecución del scheduler en un hilo separado
scheduler_thread = threading.Thread(target=monitor_and_process)
scheduler_thread.daemon = True
scheduler_thread.start()
