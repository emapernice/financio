from database.db import get_connection
from datetime import datetime

class Record:
    def __init__(
        self,
        account_id,
        subcategory_id,
        record_amount,
        record_type,
        record_description=None,
        record_date=None,
        supplier_id=None,
        exchange_id=None,
        transfer_id=None,
        created_at=None,
        record_id=None
    ):
        self.record_id = record_id
        self.account_id = account_id
        self.subcategory_id = subcategory_id
        self.record_amount = record_amount
        self.record_type = record_type
        self.record_description = record_description
        self.record_date = record_date or datetime.now()
        self.supplier_id = supplier_id
        self.exchange_id = exchange_id
        self.transfer_id = transfer_id
        self.created_at = created_at or datetime.now()

    def __str__(self):
        return f"<Record {self.record_type} ${self.record_amount} on {self.record_date}>"

    def save_to_db(self):
        with get_connection() as conn:
            with conn.cursor() as cursor:
                sql = """
                    INSERT INTO records (
                        account_id, subcategory_id, record_amount, record_type,
                        record_description, record_date, supplier_id,
                        exchange_id, transfer_id, created_at
                    ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                """
                values = (
                    self.account_id, self.subcategory_id, self.record_amount, self.record_type,
                    self.record_description, self.record_date, self.supplier_id,
                    self.exchange_id, self.transfer_id, self.created_at
                )
                cursor.execute(sql, values)
                conn.commit()
                self.record_id = cursor.lastrowid
                print(f"Record inserted with ID {self.record_id}")
                return True

    @classmethod
    def get_by_id(cls, record_id):
        with get_connection() as conn:
            with conn.cursor(dictionary=True) as cursor:
                cursor.execute("SELECT * FROM records WHERE record_id = %s", (record_id,))
                row = cursor.fetchone()
                if row:
                    return cls(**row)
                else:
                    print("Record not found.")
                    return None

    def delete_record(self):
        if not self.record_id:
            print("Cannot delete: Record has no ID.")
            return False
        with get_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute("DELETE FROM records WHERE record_id = %s", (self.record_id,))
                conn.commit()
                print("🗑️ Record deleted successfully.")
                return True
