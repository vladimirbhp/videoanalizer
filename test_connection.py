import pyodbc
import config

def get_db_connection():
    try:
        conn = pyodbc.connect(
            f"DRIVER={{{config.DB_CONFIG['DRIVER']}}};SERVER={config.DB_CONFIG['SERVER']};"
            f"DATABASE={config.DB_CONFIG['DATABASE']};UID={config.DB_CONFIG['USER']};"
            f"PWD={config.DB_CONFIG['PASSWORD']}"
        )
        print("Conexión exitosa")
        return conn
    except Exception as e:
        print(f"Error de conexión: {e}")
        return None

# Intentar la conexión
get_db_connection()
