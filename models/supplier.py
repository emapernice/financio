from database.db import get_connection
from datetime import datetime

class Supplier:
    def __init__(self, supplier_name, supplier_description=None, supplier_id=None):
        self.supplier_id = supplier_id
        self.supplier_name = supplier_name
        self.supplier_description = supplier_description

    def __str__(self):
        return f"<Supplier {self.supplier_name}>"

    def show_details(self):
        print(f"ID: {self.supplier_id}")
        print(f"Name: {self.supplier_name}")
        print(f"Description: {self.supplier_description}")

    def name_exists(self):
        conn = get_connection()
        cursor = conn.cursor()
        sql = "SELECT supplier_id FROM suppliers WHERE supplier_name = %s"
        cursor.execute(sql, (self.supplier_name,))
        result = cursor.fetchone()
        cursor.close()
        conn.close()
        return result is not None

    def save_to_db(self):
        if self.name_exists():
            print(f"Supplier name {self.supplier_name} already exists in DB. Skipping insert.")
            return False

        conn = get_connection()
        cursor = conn.cursor()
        sql = """
            INSERT INTO suppliers (supplier_name, supplier_description)
            VALUES (%s, %s)
        """
        values = (self.supplier_name, self.supplier_description)
        cursor.execute(sql, values)
        conn.commit()
        self.supplier_id = cursor.lastrowid
        cursor.close()
        conn.close()
        print(f"Supplier inserted with ID {self.supplier_id}")
        return True

    @classmethod
    def get_by_id(cls, supplier_id):
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM suppliers WHERE supplier_id = %s", (supplier_id,))
        row = cursor.fetchone()
        cursor.close()
        conn.close()
        if row:
            return cls(**row)
        else:
            print("Supplier not found.")
            return None

    @classmethod
    def get_by_name(cls, name):
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM suppliers WHERE supplier_name = %s", (name,))
        row = cursor.fetchone()
        cursor.close()
        conn.close()
        if row:
            return cls(**row)
        else:
            print("Supplier not found.")
            return None

    def update_supplier(self, new_name=None, new_description=None):
        if not self.supplier_id:
            print("Cannot update: Supplier has no ID assigned.")
            return False

        if not new_name and new_description is None:
            print("No data provided to update.")
            return False

        conn = get_connection()
        cursor = conn.cursor()
        sql = "UPDATE suppliers SET supplier_name = %s, supplier_description = %s WHERE supplier_id = %s"
        cursor.execute(sql, (
            new_name or self.supplier_name,
            new_description if new_description is not None else self.supplier_description,
            self.supplier_id
        ))
        conn.commit()
        if new_name:
            self.supplier_name = new_name
        if new_description is not None:
            self.supplier_description = new_description
        cursor.close()
        conn.close()
        print("Supplier updated successfully.")
        return True

    def delete_supplier(self):
        if not self.supplier_id:
            print("Cannot delete: Supplier has no ID assigned.")
            return False

        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM suppliers WHERE supplier_id = %s", (self.supplier_id,))
        conn.commit()
        cursor.close()
        conn.close()
        print("Supplier deleted successfully.")
        return True
