import time
import pandas as pd
import mysql.connector
from conexion import mydb
import os

# Especifica los nombres de las columnas manualmente
column_names = ['tarjeta', 'tip_prod', 'nombre', 'color', 'calibre', 'seccion', 'tipo_produccion', 'hojas', 'cliente', 'fecha']

# Función para insertar datos en la base de datos en lotes
def insert_data(df, batch_size=100):
    try:
        connection = mydb.connect()
        cursor = mydb.cursor()
        total_rows = len(df)
        for start in range(0, total_rows, batch_size):
            end = start + batch_size
            batch = df.iloc[start:end]
            values = [
                (row['tarjeta'], row['tip_prod'], row['nombre'], row['color'], row['calibre'], row['seccion'],
                    row['tipo_produccion'], row['hojas'], row['cliente'], row['fecha'])
                for index, row in batch.iterrows()
            ]
            sql = """INSERT INTO `recepcion_eco` (`tarjeta`, `tip_prod`, `nombre`, `color`, `calibre`, `seccion`, `tipo_produccion`, `hojas`, `cliente`, `fecha`)
                        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"""
            cursor.executemany(sql, values)
            connection.commit()
            print(f'Lote {start // batch_size + 1} insertado con éxito')
            time.sleep(1)  # Esperar 1 segundo entre lotes para evitar sobrecargar el servidor
        cursor.close()
        connection.close()
        print("Todos los datos insertados con éxito")
    except mysql.connector.Error as err:
        print(f"Error al insertar datos en la base de datos: {err}")
    except Exception as e:
        print(f"Error inesperado: {e}")

# Función para leer el archivo y procesar datos
def process_file(file_path):
    print(f"Procesando el archivo: {file_path}")
    try:
        # Lee el archivo .prn sin encabezados y usa los nombres de columnas especificados
        df = pd.read_csv(file_path, sep=',', header=None, names=column_names, skipinitialspace=True, engine='python')
        print("Datos leídos del archivo:")
        print(df.head())  # Imprime las primeras filas del dataframe para depuración
        
        # Verifica el número de filas leídasr
        print(f"Total de filas leídas: {len(df)}")
        
        insert_data(df)
    except pd.errors.EmptyDataError:
        print("El archivo está vacío.")
    except pd.errors.ParserError as e:
        print(f"Error al analizar el archivo: {e}")
    except Exception as e:
        print(f"Error al procesar el archivo: {e}")

# Configuración del archivo
file_path = r'\\192.168.0.114\D\compartidos\plsaldo.prn'  # Ruta completa del archivo

# Verificar si el archivo existe
if not os.path.exists(file_path):
    print(f"El archivo {file_path} no existe.")
else:
    process_file(file_path)
