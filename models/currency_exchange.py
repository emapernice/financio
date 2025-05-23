from database.db import get_connection
from datetime import datetime

class CurrencyExchange:
    def __init__(self, from_currency_id, to_currency_id, exchange_rate, exchange_date=None, exchange_id=None):
        self.exchange_id = exchange_id
        self.from_currency_id = from_currency_id
        self.to_currency_id = to_currency_id
        self.exchange_rate = exchange_rate
        self.exchange_date = exchange_date or datetime.now()

    def __str__(self):
        return f"<Exchange {self.from_currency_id} -> {self.to_currency_id} @ {self.exchange_rate}>"

    def save_to_db(self):
        conn = get_connection()
        cursor = conn.cursor()
        sql = """
            INSERT INTO currency_exchange (from_currency_id, to_currency_id, exchange_rate, exchange_date)
            VALUES (%s, %s, %s, %s)
        """
        values = (self.from_currency_id, self.to_currency_id, self.exchange_rate, self.exchange_date)
        cursor.execute(sql, values)
        conn.commit()
        self.exchange_id = cursor.lastrowid
        cursor.close()
        conn.close()
        print(f"Exchange inserted with ID {self.exchange_id}")
        return True

    @classmethod
    def get_by_id(cls, exchange_id):
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM currency_exchange WHERE exchange_id = %s", (exchange_id,))
        row = cursor.fetchone()
        cursor.close()
        conn.close()
        if row:
            return cls(**row)
        else:
            print("Exchange not found.")
            return None

    def delete_exchange(self):
        if not self.exchange_id:
            print("Cannot delete: Exchange has no ID.")
            return False
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM currency_exchange WHERE exchange_id = %s", (self.exchange_id,))
        conn.commit()
        cursor.close()
        conn.close()
        print("Exchange deleted successfully.")
        return True
