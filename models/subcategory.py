from database.db import get_connection
from datetime import datetime

class Subcategory:
    def __init__(self, subcategory_name, category_id, created_at=None, subcategory_id=None):
        self.subcategory_id = subcategory_id
        self.subcategory_name = subcategory_name
        self.category_id = category_id
        self.created_at = created_at or datetime.now()

    def __str__(self):
        return f"<Subcategory {self.subcategory_name} (Category ID: {self.category_id})>"

    def show_details(self):
        print(f"ID: {self.subcategory_id}")
        print(f"Name: {self.subcategory_name}")
        print(f"Category ID: {self.category_id}")
        print(f"Creation date: {self.created_at}")

    def name_exists(self):
        conn = get_connection()
        cursor = conn.cursor()
        sql = "SELECT subcategory_id FROM subcategories WHERE subcategory_name = %s AND category_id = %s"
        cursor.execute(sql, (self.subcategory_name, self.category_id))
        result = cursor.fetchone()
        cursor.close()
        conn.close()
        return result is not None

    def save_to_db(self):
        if self.name_exists():
            print(f"⚠️ Subcategory name {self.subcategory_name} already exists in DB for category {self.category_id}. Skipping insert.")
            return False

        conn = get_connection()
        cursor = conn.cursor()
        sql = """
            INSERT INTO subcategories (subcategory_name, category_id)
            VALUES (%s, %s)
        """
        values = (self.subcategory_name, self.category_id)
        cursor.execute(sql, values)
        conn.commit()
        self.subcategory_id = cursor.lastrowid
        cursor.close()
        conn.close()
        print(f"✅ Subcategory inserted with ID {self.subcategory_id}")
        return True

    @classmethod
    def get_by_id(cls, subcategory_id):
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM subcategories WHERE subcategory_id = %s", (subcategory_id,))
        row = cursor.fetchone()
        cursor.close()
        conn.close()
        if row:
            return cls(**row)
        else:
            print("❌ Subcategory not found.")
            return None
        
    @classmethod
    def get_by_name_and_category(cls, name, category_id):
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        sql = "SELECT * FROM subcategories WHERE subcategory_name = %s AND category_id = %s"
        cursor.execute(sql, (name, category_id))
        row = cursor.fetchone()
        cursor.close()
        conn.close()
        if row:
            return cls(**row)
        else:
            print("❌ Subcategory not found.")
            return None    

    def update_subcategory(self, new_name=None, new_category_id=None):
        if not self.subcategory_id:
            print("❌ Cannot update: Subcategory has no ID assigned.")
            return False

        if not new_name and not new_category_id:
            print("⚠️ No new data provided.")
            return False

        if new_name:
            self.subcategory_name = new_name
        if new_category_id:
            self.category_id = new_category_id

        conn = get_connection()
        cursor = conn.cursor()
        sql = "UPDATE subcategories SET subcategory_name = %s, category_id = %s WHERE subcategory_id = %s"
        cursor.execute(sql, (self.subcategory_name, self.category_id, self.subcategory_id))
        conn.commit()
        cursor.close()
        conn.close()
        print("✅ Subcategory updated successfully.")
        return True

    def delete_subcategory(self):
        if not self.subcategory_id:
            print("❌ Cannot delete: Subcategory has no ID assigned.")
            return False

        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM subcategories WHERE subcategory_id = %s", (self.subcategory_id,))
        conn.commit()
        cursor.close()
        conn.close()
        print("🗑️ Subcategory deleted successfully.")
        return True