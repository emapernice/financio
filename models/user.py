from database.db import get_connection
from datetime import datetime

class User:
    def __init__(self, user_name, user_email, created_at=None, user_id=None):
        self.user_id = user_id
        self.user_name = user_name
        self.user_email = user_email
        self.created_at = created_at or datetime.now()

    def __str__(self):
        return f"<User {self.user_name} ({self.user_email})>"

    def show_details(self):
        print(f"ID: {self.user_id}")
        print(f"Name: {self.user_name}")
        print(f"Email: {self.user_email}")
        print(f"Creation date: {self.created_at}")

    def email_exists(self):
        conn = get_connection()
        cursor = conn.cursor()
        sql = "SELECT user_id FROM users WHERE user_email = %s"
        cursor.execute(sql, (self.user_email,))
        result = cursor.fetchone()
        cursor.close()
        conn.close()
        return result is not None

    def save_to_db(self):
        if self.email_exists():
            print(f"⚠️ Email {self.user_email} already exists in DB. Skipping insert.")
            return False

        conn = get_connection()
        cursor = conn.cursor()
        sql = """
            INSERT INTO users (user_name, user_email)
            VALUES (%s, %s)
        """
        values = (self.user_name, self.user_email)
        cursor.execute(sql, values)
        conn.commit()
        self.user_id = cursor.lastrowid
        cursor.close()
        conn.close()
        print(f"✅ User inserted with ID {self.user_id}")
        return True

    @classmethod
    def get_by_id(cls, user_id):
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM users WHERE user_id = %s", (user_id,))
        row = cursor.fetchone()
        cursor.close()
        conn.close()
        if row:
            return cls(**row)
        else:
            print("❌ User not found.")
            return None

    @classmethod
    def get_by_email(cls, email):
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM users WHERE user_email = %s", (email,))
        row = cursor.fetchone()
        cursor.close()
        conn.close()
        if row:
            return cls(**row)
        else:
            print("❌ User not found.")
            return None

    def update_user(self, new_name=None, new_email=None):
        if not self.user_id:
            print("❌ Cannot update: User has no ID assigned.")
            return False

        conn = get_connection()
        cursor = conn.cursor()

        updates = []
        values = []

        if new_name:
            updates.append("user_name = %s")
            values.append(new_name)
            self.user_name = new_name

        if new_email:
            cursor.execute("SELECT user_id FROM users WHERE user_email = %s AND user_id != %s", (new_email, self.user_id))
            if cursor.fetchone():
                print(f"⚠️ The email {new_email} is already in use by another user.")
                cursor.close()
                conn.close()
                return False
            updates.append("user_email = %s")
            values.append(new_email)
            self.user_email = new_email

        if not updates:
            print("⚠️ There are no fields to update.")
            cursor.close()
            conn.close()
            return False

        values.append(self.user_id)
        sql = f"UPDATE users SET {', '.join(updates)} WHERE user_id = %s"
        cursor.execute(sql, values)
        conn.commit()
        cursor.close()
        conn.close()
        print("✅ User updated successfully.")
        return True

    def delete_user(self):
        if not self.user_id:
            print("❌ Cannot delete: User has no ID assigned.")
            return False

        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM users WHERE user_id = %s", (self.user_id,))
        conn.commit()
        cursor.close()
        conn.close()
        print("🗑️ User deleted successfully.")
        return True
