import os
import mysql.connector
from mysql.connector import Error
from dotenv import load_dotenv

load_dotenv()

def connect_db():
    """Estabelece e retorna a conexão com o banco de dados MySQL usando variáveis de ambiente."""
    try:
        conn = mysql.connector.connect(
            host=os.getenv('DB_HOST', 'localhost'),
            user=os.getenv('DB_USER', 'root'),
            password=os.getenv('DB_PASSWORD', ''),
            database=os.getenv('DB_NAME', 'imoveis_db'),
            port=int(os.getenv('DB_PORT', 3306))
        )
        if conn.is_connected():
            return conn
    except Error as err:
        print(f"Erro de conexão MySQL: {err}")
        return None
