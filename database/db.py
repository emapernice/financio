import mysql.connector
from config import DB_CONFIG

def get_connection():
    return mysql.connector.connect(**DB_CONFIG)

if __name__ == "__main__":
    conn = get_connection()
    print("Conexión exitosa:", conn.is_connected())
    conn.close()
