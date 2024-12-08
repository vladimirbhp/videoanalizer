from config import get_db_connection

def check_tables():
    """Verifica las tablas existentes en la base de datos."""
    try:
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT TABLE_NAME FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_TYPE = 'BASE TABLE'")
            tables = cursor.fetchall()
            if tables:
                print("Tablas existentes en la base de datos:")
                for table in tables:
                    print(f"- {table[0]}")
            else:
                print("No se encontraron tablas en la base de datos.")
    except Exception as e:
        print(f"Error al verificar las tablas: {e}")

def insert_test_data():
    """Inserta datos de prueba en las tablas Analisis y DetallesErrores."""
    try:
        with get_db_connection() as conn:
            cursor = conn.cursor()
            
            # Insertar en Analisis
            cursor.execute("""
                INSERT INTO Analisis (video_nombre, video_url, errores_fotograma, errores_audio)
                VALUES (?, ?, ?, ?)
            """, ("video_prueba.mp4", "http://urlvideo1.com", 10, 5))
            analisis_id = cursor.execute("SELECT SCOPE_IDENTITY()").fetchval()  # Obtener el último ID insertado
            
            # Insertar en DetallesErrores
            cursor.execute("""
                INSERT INTO DetallesErrores (analisis_id, tipo_error, minuto, descripcion)
                VALUES (?, ?, ?, ?)
            """, (analisis_id, "Error de fotograma", 3, "Frame missing at 3:00"))
            
            cursor.execute("""
                INSERT INTO DetallesErrores (analisis_id, tipo_error, minuto, descripcion)
                VALUES (?, ?, ?, ?)
            """, (analisis_id, "Error de audio", 5, "Audio distortion at 5:00"))
            
            conn.commit()
            print("Datos de prueba insertados en las tablas Analisis y DetallesErrores.")
    except Exception as e:
        print(f"Error al insertar datos de prueba: {e}")

def fetch_test_data():
    """Obtiene datos de prueba de las tablas."""
    try:
        with get_db_connection() as conn:
            cursor = conn.cursor()
            
            # Obtener datos de la tabla Analisis
            cursor.execute("SELECT * FROM Analisis")
            rows = cursor.fetchall()
            print("Datos en la tabla Analisis:")
            for row in rows:
                print(row)
            
            # Obtener datos de la tabla DetallesErrores
            cursor.execute("SELECT * FROM DetallesErrores")
            rows = cursor.fetchall()
            print("\nDatos en la tabla DetallesErrores:")
            for row in rows:
                print(row)
                
    except Exception as e:
        print(f"Error al obtener datos: {e}")

if __name__ == "__main__":
    print("=== Verificando Tablas ===")
    check_tables()
    print("\n=== Insertando Datos de Prueba ===")
    insert_test_data()
    print("\n=== Obteniendo Datos de las Tablas ===")
    fetch_test_data()
