# app.py

from database.db import get_connection

def main():
    conn = get_connection()
    if conn.is_connected():
        print("Successful connection to the database.")
        conn.close()
    else:
        print("Could not connect.")

if __name__ == "__main__":
    main()
