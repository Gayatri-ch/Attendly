import os

class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY") or "attendly_secret_key"
    UPLOAD_FOLDER = "students"
    
    # Database Settings
    DB_HOST = "localhost"
    DB_USER = "root"
    DB_PASSWORD = "root"
    DB_NAME = "attendly_db"

    # AI Settings
    FACE_RECOGNITION_MODEL = "Facenet512"
    DETECTOR_BACKEND = "retinaface"
    SIMILARITY_THRESHOLD = 0.4 # Lower is more strict
