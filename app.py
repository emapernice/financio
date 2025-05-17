# app.py

from database.db import get_connection

def main():
    conn = get_connection()
    if conn.is_connected():
        print("Conexión exitosa a la base de datos.")
        conn.close()
    else:
        print("No se pudo conectar.")

if __name__ == "__main__":
    main()
