from database.db import get_connection
from datetime import datetime

class Category:
    def __init__(self, category_name, category_type, created_at=None, category_id=None):
        self.category_id = category_id
        self.category_name = category_name
        self.category_type = category_type
        self.created_at = created_at or datetime.now()

    def __str__(self):
        return f"<Category {self.category_name} ({self.category_type})>"

    def show_details(self):
        print(f"ID: {self.category_id}")
        print(f"Name: {self.category_name}")
        print(f"Type: {self.category_type}")
        print(f"Creation date: {self.created_at}")

    def name_exists(self):
        conn = get_connection()
        cursor = conn.cursor()
        sql = "SELECT category_id FROM categories WHERE category_name = %s"
        cursor.execute(sql, (self.category_name,))
        result = cursor.fetchone()
        cursor.close()
        conn.close()
        return result is not None

    def save_to_db(self):
        if self.name_exists():
            print(f"⚠️ Category name {self.category_name} already exists in DB. Skipping insert.")
            return False

        conn = get_connection()
        cursor = conn.cursor()
        sql = """
            INSERT INTO categories (category_name, category_type)
            VALUES (%s, %s)
        """
        values = (self.category_name, self.category_type)
        cursor.execute(sql, values)
        conn.commit()
        self.category_id = cursor.lastrowid
        cursor.close()
        conn.close()
        print(f"Category inserted with ID {self.category_id}")
        return True

    @classmethod
    def get_by_id(cls, category_id):
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM categories WHERE category_id = %s", (category_id,))
        row = cursor.fetchone()
        cursor.close()
        conn.close()
        if row:
            return cls(**row)
        else:
            print("Category not found.")
            return None

    @classmethod
    def get_by_name(cls, name):
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM categories WHERE category_name = %s", (name,))
        row = cursor.fetchone()
        cursor.fetchall() 
        cursor.close()
        conn.close()
        if row:
            return cls(**row)
        else:
            print("Category not found.")
            return None

    def update_category(self, new_name=None, new_type=None):
        if not self.category_id:
            print("Cannot update: Category has no ID assigned.")
            return False

        if not new_name and not new_type:
            print("No new data provided.")
            return False

        conn = get_connection()
        cursor = conn.cursor()

        if new_name:
            self.category_name = new_name
        if new_type:
            self.category_type = new_type

        sql = "UPDATE categories SET category_name = %s, category_type = %s WHERE category_id = %s"
        cursor.execute(sql, (self.category_name, self.category_type, self.category_id))
        conn.commit()
        cursor.close()
        conn.close()
        print("Category updated successfully.")
        return True

    def delete_category(self):
        if not self.category_id:
            print("Cannot delete: Category has no ID assigned.")
            return False

        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("DELETE FROM subcategories WHERE category_id = %s", (self.category_id,))
        print("Related subcategories deleted.")

        cursor.execute("DELETE FROM categories WHERE category_id = %s", (self.category_id,))
        conn.commit()
        cursor.close()
        conn.close()
        print("Category deleted successfully.")
        return True
