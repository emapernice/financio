from database.db import get_connection
from datetime import datetime

class Currency:
    def __init__(self, currency_code, currency_name, created_at=None, currency_id=None):
        self.currency_id = currency_id
        self.currency_code = currency_code
        self.currency_name = currency_name
        self.created_at = created_at or datetime.now()

    def __str__(self):
        return f"<Currency {self.currency_code} ({self.currency_name})>"

    def show_details(self):
        print(f"ID: {self.currency_id}")
        print(f"Code: {self.currency_code}")
        print(f"Name: {self.currency_name}")
        print(f"Creation date: {self.created_at}")

    def code_exists(self):
        conn = get_connection()
        cursor = conn.cursor()
        sql = "SELECT currency_id FROM currencies WHERE currency_code = %s"
        cursor.execute(sql, (self.currency_code,))
        result = cursor.fetchone()
        cursor.close()
        conn.close()
        return result is not None

    def save_to_db(self):
        if self.code_exists():
            print(f"⚠️ Currency code {self.currency_code} already exists in DB. Skipping insert.")
            return False

        conn = get_connection()
        cursor = conn.cursor()
        sql = """
            INSERT INTO currencies (currency_code, currency_name)
            VALUES (%s, %s)
        """
        values = (self.currency_code, self.currency_name)
        cursor.execute(sql, values)
        conn.commit()
        self.currency_id = cursor.lastrowid
        cursor.close()
        conn.close()
        print(f"✅ Currency inserted with ID {self.currency_id}")
        return True

    @classmethod
    def get_by_id(cls, currency_id):
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM currencies WHERE currency_id = %s", (currency_id,))
        row = cursor.fetchone()
        cursor.close()
        conn.close()
        if row:
            return cls(**row)
        else:
            print("❌ Currency not found.")
            return None

    @classmethod
    def get_by_code(cls, code):
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM currencies WHERE currency_code = %s", (code,))
        row = cursor.fetchone()
        cursor.close()
        conn.close()
        if row:
            return cls(**row)
        else:
            print("❌ Currency not found.")
            return None

    def update_currency(self, new_name=None):
        if not self.currency_id:
            print("❌ Cannot update: Currency has no ID assigned.")
            return False

        if not new_name:
            print("⚠️ No new name provided.")
            return False

        conn = get_connection()
        cursor = conn.cursor()
        sql = "UPDATE currencies SET currency_name = %s WHERE currency_id = %s"
        cursor.execute(sql, (new_name, self.currency_id))
        conn.commit()
        self.currency_name = new_name
        cursor.close()
        conn.close()
        print("✅ Currency updated successfully.")
        return True

    def delete_currency(self):
        if not self.currency_id:
            print("❌ Cannot delete: Currency has no ID assigned.")
            return False

        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM currencies WHERE currency_id = %s", (self.currency_id,))
        conn.commit()
        cursor.close()
        conn.close()
        print("🗑️ Currency deleted successfully.")
        return True