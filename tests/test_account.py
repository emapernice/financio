import unittest
from datetime import datetime
from models.account import Account
from models.currency import Currency
from models.user import User

class TestAccountModel(unittest.TestCase):
    def setUp(self):
        self.user = User.get_by_email("test@user.com")
        if not self.user:
            self.user = User(user_name="Test User", user_email="test@user.com")
            self.user.save_to_db()

        self.currency = Currency.get_by_code("ARS")
        if not self.currency:
            self.currency = Currency("ARS", "Argentine peso")
            self.currency.save_to_db()

        self.account = Account(
            account_name="Current account",
            account_type="Bank",
            currency_id=self.currency.currency_id,
            initial_balance=15000.00,
            user_id=self.user.user_id,
            created_at=datetime(2024, 5, 20)
        )
        self.account.save_to_db()

    def test_insert_and_get_account(self):
        retrieved = Account.get_by_id(self.account.account_id)
        self.assertIsNotNone(retrieved)
        self.assertEqual(retrieved.account_name, self.account.account_name)
        self.assertEqual(retrieved.currency_id, self.currency.currency_id)
        self.assertEqual(retrieved.user_id, self.user.user_id)

    def test_update_account(self):
        updated = self.account.update_account(
            account_name="Updated account",
            account_type="Box",
            initial_balance=9999.99
        )
        self.assertTrue(updated)

        retrieved = Account.get_by_id(self.account.account_id)
        self.assertEqual(retrieved.account_name, "Updated account")
        self.assertEqual(retrieved.account_type, "Box")
        self.assertAlmostEqual(float(retrieved.initial_balance), 9999.99, places=2)

    def test_delete_account(self):
        temp_account = Account(
            account_name="Temporary",
            account_type="Cash",
            currency_id=self.currency.currency_id,
            initial_balance=500.00,
            user_id=self.user.user_id
        )
        temp_account.save_to_db()
        self.assertTrue(temp_account.delete_account())
        self.assertIsNone(Account.get_by_id(temp_account.account_id))

    def tearDown(self):
        if self.account:
            self.account.delete_account()

if __name__ == "__main__":
    unittest.main()
