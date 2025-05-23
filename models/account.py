from database.db import get_connection
from datetime import datetime

class Account:
    def __init__(self, account_name, account_type, currency_id, initial_balance, user_id, created_at=None, account_id=None):
        self.account_id = account_id
        self.account_name = account_name
        self.account_type = account_type
        self.currency_id = currency_id
        self.initial_balance = initial_balance
        self.user_id = user_id
        self.created_at = created_at or datetime.now()

    def __str__(self):
        return f"<Account {self.account_name} ({self.account_type})>"

    def save_to_db(self):
        conn = get_connection()
        try:
            with conn.cursor() as cursor:
                sql = """
                    INSERT INTO accounts (account_name, account_type, currency_id, initial_balance, user_id, created_at)
                    VALUES (%s, %s, %s, %s, %s, %s)
                """
                values = (
                    self.account_name,
                    self.account_type,
                    self.currency_id,
                    self.initial_balance,
                    self.user_id,
                    self.created_at
                )
                cursor.execute(sql, values)
                conn.commit()
                self.account_id = cursor.lastrowid
                print(f"Account inserted with ID {self.account_id}")
                return True
        finally:
            conn.close()

    @classmethod
    def get_by_id(cls, account_id):
        conn = get_connection()
        try:
            with conn.cursor(dictionary=True) as cursor:
                cursor.execute("SELECT * FROM accounts WHERE account_id = %s", (account_id,))
                row = cursor.fetchone()
                if row:
                    return cls(**row)
                else:
                    print("Account not found.")
                    return None
        finally:
            conn.close()

    def update_account(self, account_name=None, account_type=None, initial_balance=None):
        if not self.account_id:
            print("Cannot update: Account has no ID.")
            return False

        updates = []
        values = []

        if account_name is not None:
            updates.append("account_name = %s")
            values.append(account_name)
            self.account_name = account_name

        if account_type is not None:
            updates.append("account_type = %s")
            values.append(account_type)
            self.account_type = account_type

        if initial_balance is not None:
            updates.append("initial_balance = %s")
            values.append(initial_balance)
            self.initial_balance = initial_balance

        if not updates:
            print("Nothing to update.")
            return False

        values.append(self.account_id)

        sql = f"UPDATE accounts SET {', '.join(updates)} WHERE account_id = %s"

        conn = get_connection()
        try:
            with conn.cursor() as cursor:
                cursor.execute(sql, tuple(values))
                conn.commit()
                print(f"Account {self.account_id} updated successfully.")
                return True
        finally:
            conn.close()

    def delete_account(self):
        if not self.account_id:
            print("Cannot delete: Account has no ID.")
            return False
        conn = get_connection()
        try:
            with conn.cursor() as cursor:
                cursor.execute("DELETE FROM accounts WHERE account_id = %s", (self.account_id,))
                conn.commit()
                print("Account deleted successfully.")
                return True
        finally:
            conn.close()
