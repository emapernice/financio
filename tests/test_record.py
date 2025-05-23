import unittest
from datetime import datetime

from models.record import Record
from models.user import User
from models.currency import Currency
from models.account import Account
from models.supplier import Supplier
from models.category import Category
from models.subcategory import Subcategory
from models.currency_exchange import CurrencyExchange
from models.transfer import Transfer

class TestRecordModel(unittest.TestCase):
    def setUp(self):
        self.user = User.get_by_email("record@test.com")
        if not self.user:
            self.user = User("Record Tester", "record@test.com")
            self.user.save_to_db()

        self.currency = Currency.get_by_code("USD")
        if not self.currency:
            self.currency = Currency("USD", "US Dollar")
            self.currency.save_to_db()

        self.account = Account("Test Account", "current", self.currency.currency_id, 1000, self.user.user_id)
        self.account.save_to_db()

        self.supplier = Supplier("Test Supplier", "Test supplier")
        self.supplier.save_to_db()

        self.category = Category.get_by_name("Test Category")
        if not self.category:
            self.category = Category("Test Category", "expense")
            self.category.save_to_db()

        self.subcategory = Subcategory.get_by_name_and_category("Test Subcategory", self.category.category_id)
        if not self.subcategory:
            self.subcategory = Subcategory("Test Subcategory", self.category.category_id)
            self.subcategory.save_to_db()

        assert self.subcategory.subcategory_id is not None, "Subcategory ID is None!"

        self.exchange = CurrencyExchange(self.currency.currency_id, self.currency.currency_id, 1.0)
        self.exchange.save_to_db()

        self.account_to = Account("Destination", "saving", self.currency.currency_id, 500, self.user.user_id)
        self.account_to.save_to_db()
        self.transfer = Transfer(self.account.account_id, self.account_to.account_id, 200.0)
        self.transfer.save_to_db()

        self.record = Record(
            account_id=self.account.account_id,
            subcategory_id=self.subcategory.subcategory_id,
            record_amount=123.45,
            record_type="expense",
            record_description="Test expense",
            record_date=datetime(2024, 5, 20),
            supplier_id=self.supplier.supplier_id,
            exchange_id=self.exchange.exchange_id,
            transfer_id=self.transfer.transfer_id
        )
        self.record.save_to_db()

    def test_insert_and_get_record(self):
        retrieved = Record.get_by_id(self.record.record_id)
        self.assertIsNotNone(retrieved)
        self.assertEqual(retrieved.account_id, self.account.account_id)
        self.assertEqual(retrieved.record_type, "expense")
        self.assertAlmostEqual(float(retrieved.record_amount), 123.45, places=2)
        self.assertEqual(retrieved.supplier_id, self.supplier.supplier_id)

    def test_delete_record(self):
        record_to_delete = Record(
            account_id=self.account.account_id,
            subcategory_id=self.subcategory.subcategory_id,
            record_amount=50.0,
            record_type="income",
            record_description="Temporary income",
            record_date=datetime.now()
        )
        record_to_delete.save_to_db()
        deleted = record_to_delete.delete_record()
        self.assertTrue(deleted)
        self.assertIsNone(Record.get_by_id(record_to_delete.record_id))

if __name__ == "__main__":
    unittest.main()
