import os
from azure.storage.blob import BlobServiceClient
from dotenv import load_dotenv

# Cargar variables de entorno desde el archivo .env
load_dotenv()

# Obtener la cadena de conexión desde .env
connection_string = os.getenv("AZURE_STORAGE_CONNECTION_STRING")

# Crear el cliente de servicio Blob
try:
    blob_service_client = BlobServiceClient.from_connection_string(connection_string)
    print("Conexión a Azure Blob Storage exitosa.")
    
    # Listar contenedores disponibles
    containers = blob_service_client.list_containers()
    print("Contenedores disponibles:")
    for container in containers:
        print(f"- {container.name}")
except Exception as e:
    print(f"Error al conectar con Azure Blob Storage: {e}")
