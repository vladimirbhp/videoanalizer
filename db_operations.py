import pyodbc

def connect_to_database():
    try:
        conn = pyodbc.connect(
            "Driver={ODBC Driver 18 for SQL Server};"
            "Server=tcp:videodataser.database.windows.net,1433;"
            "Database=videodata;"
            "Uid=grupo6;"
            "Pwd=videoanalizer1.;"
            "Encrypt=yes;"
            "TrustServerCertificate=no;"
            "Connection Timeout=30;"
        )
        return conn
    except pyodbc.Error as e:
        print(f"Error al conectar a la base de datos: {e}")
        return None

def fetch_all_from_table(table_name):
    conn = connect_to_database()
    if conn:
        cursor = conn.cursor()
        cursor.execute(f"SELECT * FROM {table_name}")
        rows = cursor.fetchall()
        conn.close()
        return rows
    else:
        return []

# Uso
if __name__ == "__main__":
    rows = fetch_all_from_table("Analisis")
    for row in rows:
        print(row)
