# config.py

from dotenv import load_dotenv
import os

# Cargar las variables desde el archivo .env
load_dotenv()

# Configuración de Azure Blob Storage
BLOB_STORAGE_CONNECTION_STRING = os.getenv("AZURE_STORAGE_CONNECTION_STRING")
BLOB_CONTAINER_NAME = os.getenv("BLOB_CONTAINER_NAME")

# Configuración de la base de datos SQL Server
DB_CONFIG = {
    "DRIVER": os.getenv("DB_DRIVER"),
    "SERVER": os.getenv("DB_SERVER"),
    "DATABASE": os.getenv("DB_DATABASE"),
    "USER": os.getenv("DB_USER"),
    "PASSWORD": os.getenv("DB_PASSWORD")
}

# Configuración de otros parámetros
UPLOAD_FOLDER = os.getenv("UPLOAD_FOLDER")
DEBUG = os.getenv("DEBUG", "False") == "True"  # Convierte a Booleano
SECRET_KEY = os.getenv("SECRET_KEY")
