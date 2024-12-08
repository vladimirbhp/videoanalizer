from flask import Flask, request, redirect, url_for, flash, render_template
from werkzeug.utils import secure_filename
import os
from azure.storage.blob import BlobServiceClient
import config
from test_connection import get_db_connection
from analysis.video_utils import VideoUtils  # Importa VideoUtils desde la carpeta analysis

app = Flask(__name__)

# Configuración de la ruta de carga de videos localmente
app.config['UPLOAD_FOLDER'] = config.UPLOAD_FOLDER
app.config['ALLOWED_EXTENSIONS'] = {'mp4', 'mov', 'avi', 'mkv'}
app.config['SECRET_KEY'] = config.SECRET_KEY

# Crear el cliente de Azure Blob Storage usando la cadena de conexión del archivo .env
blob_service_client = BlobServiceClient.from_connection_string(config.BLOB_STORAGE_CONNECTION_STRING)
container_client = blob_service_client.get_container_client(config.BLOB_CONTAINER_NAME)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

@app.route('/')
def index():
    return render_template('index.html')  # Renderiza la plantilla index.html

@app.route('/upload', methods=['POST'])  # Esta es la ruta correcta para manejar el formulario
def upload_video():
    if 'video' not in request.files:
        flash('No se seleccionó ningún archivo.')
        return redirect(url_for('index'))

    video_file = request.files['video']
    if video_file.filename == '':
        flash('No se seleccionó ningún archivo.')
        return redirect(url_for('index'))

    if video_file and allowed_file(video_file.filename):
        filename = secure_filename(video_file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        video_file.save(filepath)

        # Subir el video a Azure Blob Storage
        blob_client = container_client.get_blob_client(filename)
        with open(filepath, "rb") as data:
            blob_client.upload_blob(data, overwrite=True)

        # URL del video en Azure Blob Storage
        video_url = f"https://{config.BLOB_STORAGE_ACCOUNT}.blob.core.windows.net/{config.BLOB_CONTAINER_NAME}/{filename}"

        # Análisis del video
        video_utils = VideoUtils(config.DB_CONFIG)
        video_errors = video_utils.analyze_video(filepath)
        audio_errors = video_utils.analyze_audio(filepath)

        # Guardar los resultados en la base de datos
        video_utils.save_results_to_db(filename, video_url, video_errors, audio_errors)

        return redirect(url_for('results', filename=filename))

@app.route('/results')
def results():
    filename = request.args.get('filename', None)
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        # Obtener el análisis principal
        cursor.execute("SELECT id FROM Analisis WHERE filename = ?", filename)
        analisis_id = cursor.fetchone()[0]

        # Obtener detalles de errores
        cursor.execute(
            "SELECT tipo, descripcion FROM DetallesErrores WHERE analisis_id = ?", 
            analisis_id
        )
        errors = [{"tipo": row[0], "descripcion": row[1]} for row in cursor.fetchall()]
    except Exception as e:
        errors = []
        flash(f"Error al obtener los resultados: {e}")
    finally:
        conn.close()

    return render_template('results.html', filename=filename, errors=errors)

if __name__ == "__main__":
    app.run(debug=config.DEBUG)
