import mysql.connector
from config import Config

def get_db_connection():
    """Returns a MySQL connection and buffered dictionary cursor."""
    conn = mysql.connector.connect(
        host=Config.DB_HOST,
        user=Config.DB_USER,
        password=Config.DB_PASSWORD,
        database=Config.DB_NAME,
        use_pure=True
    )
    return conn, conn.cursor(dictionary=True, buffered=True)
