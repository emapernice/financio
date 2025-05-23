from database.db import get_connection
from datetime import datetime

class Transfer:
    def __init__(self, account_id_from, account_id_to, transfer_amount, created_at=None, transfer_id=None):
        self.transfer_id = transfer_id
        self.account_id_from = account_id_from
        self.account_id_to = account_id_to
        self.transfer_amount = transfer_amount
        self.created_at = created_at or datetime.now()

    def __str__(self):
        return f"<Transfer {self.account_id_from} → {self.account_id_to} : ${self.transfer_amount}>"

    def save_to_db(self):
        with get_connection() as conn:
            with conn.cursor() as cursor:
                sql = """
                    INSERT INTO transfers (account_id_from, account_id_to, transfer_amount, created_at)
                    VALUES (%s, %s, %s, %s)
                """
                values = (self.account_id_from, self.account_id_to, self.transfer_amount, self.created_at)
                cursor.execute(sql, values)
                conn.commit()
                self.transfer_id = cursor.lastrowid
                print(f"Transfer inserted with ID {self.transfer_id}")
                return True

    @classmethod
    def get_by_id(cls, transfer_id):
        with get_connection() as conn:
            with conn.cursor(dictionary=True) as cursor:
                cursor.execute("SELECT * FROM transfers WHERE transfer_id = %s", (transfer_id,))
                row = cursor.fetchone()
                if row:
                    return cls(**row)
                else:
                    print("Transfer not found.")
                    return None

    def delete_transfer(self):
        if not self.transfer_id:
            print("Cannot delete: Transfer has no ID.")
            return False
        with get_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute("DELETE FROM transfers WHERE transfer_id = %s", (self.transfer_id,))
                conn.commit()
                print("Transfer deleted successfully.")
                return True
