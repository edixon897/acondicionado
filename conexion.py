
import mysql.connector
from mysql.connector import Error

def create_connection():
    """Establece una conexión a la base de datos MySQL."""
    connection = None
    try:
        connection = mysql.connector.connect(
            host="192.168.0.31",
            user="curti",
            password="Curti2025",
            database="acondicionado"
        )
        if connection.is_connected():
            print("Conexión exitosa a la base de datos")
        return connection
    except Error as e:
        print(f"Error al conectar a la base de datos: {e}")
        return None

def close_connection(connection):
    """Cierra la conexión a la base de datos."""
    if connection.is_connected():
        connection.close()
        print("Conexión cerrada")