import cv2
import librosa
import numpy as np
import pyodbc

class VideoUtils:
    def __init__(self, db_config):
        self.db_config = db_config

    def connect_db(self):
        """Establece conexión a la base de datos."""
        return pyodbc.connect(
            f"DRIVER={{{self.db_config['DRIVER']}}};SERVER={self.db_config['SERVER']};"
            f"DATABASE={self.db_config['DATABASE']};UID={self.db_config['USER']};"
            f"PWD={self.db_config['PASSWORD']};Encrypt=yes;TrustServerCertificate=no;"
        )

    def analyze_video(self, video_path):
        """Analiza frames en un video."""
        video_capture = cv2.VideoCapture(video_path)
        frame_errors = []
        frame_index = 0

        while True:
            ret, frame = video_capture.read()
            if not ret:
                break

            # Detecta frames negros como ejemplo
            if frame.mean() < 10:
                frame_errors.append(f"Frame {frame_index} es completamente negro.")

            frame_index += 1

        video_capture.release()
        return frame_errors

    def analyze_audio(self, video_path):
        """Analiza errores en el audio del video."""
        try:
            y, sr = librosa.load(video_path, sr=None, mono=True)
            rms = librosa.feature.rms(y=y)[0]
            silent_frames = np.where(rms < 0.01)[0]
            return [f"Frame de audio {frame} tiene RMS bajo." for frame in silent_frames]
        except Exception as e:
            return [f"Error al analizar el audio: {e}"]

    def save_results_to_db(self, filename, url, video_errors, audio_errors):
        """Guarda los resultados del análisis en las tablas Analisis y DetallesErrores."""
        conn = self.connect_db()
        cursor = conn.cursor()

        try:
            # Guardar el análisis principal en la tabla Analisis
            cursor.execute(
                "INSERT INTO Analisis (filename, url) VALUES (?, ?)", 
                filename, 
                url
            )
            analisis_id = cursor.execute("SELECT @@IDENTITY").fetchone()[0]

            # Guardar errores de video en DetallesErrores
            for error in video_errors:
                cursor.execute(
                    "INSERT INTO DetallesErrores (analisis_id, tipo, descripcion) VALUES (?, ?, ?)", 
                    analisis_id, 
                    'Video', 
                    error
                )

            # Guardar errores de audio en DetallesErrores
            for error in audio_errors:
                cursor.execute(
                    "INSERT INTO DetallesErrores (analisis_id, tipo, descripcion) VALUES (?, ?, ?)", 
                    analisis_id, 
                    'Audio', 
                    error
                )

            conn.commit()
        except Exception as e:
            print(f"Error al guardar los resultados: {e}")
        finally:
            conn.close()
