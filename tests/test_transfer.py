import unittest
from models.transfer import Transfer
from models.user import User
from models.currency import Currency
from models.account import Account
from datetime import datetime

class TestTransferModel(unittest.TestCase):
    def setUp(self):
        self.user = User.get_by_email("transfer@test.com")
        if not self.user:
            self.user = User("Transfer Tester", "transfer@test.com")
            self.user.save_to_db()

        self.currency = Currency.get_by_code("USD")
        if not self.currency:
            self.currency = Currency("USD", "US Dollar")
            self.currency.save_to_db()

        self.account_from = Account("Origin Account", "saving", self.currency.currency_id, 1000, self.user.user_id)
        self.account_from.save_to_db()

        self.account_to = Account("Destination Account", "current", self.currency.currency_id, 500, self.user.user_id)
        self.account_to.save_to_db()

        self.transfer = Transfer(
            account_id_from=self.account_from.account_id,
            account_id_to=self.account_to.account_id,
            transfer_amount=250.75,
            created_at=datetime(2024, 5, 20)
        )
        self.transfer.save_to_db()

    def test_insert_and_get_transfer(self):
        retrieved = Transfer.get_by_id(self.transfer.transfer_id)
        self.assertIsNotNone(retrieved)
        self.assertEqual(retrieved.account_id_from, self.account_from.account_id)
        self.assertEqual(retrieved.account_id_to, self.account_to.account_id)
        self.assertAlmostEqual(float(retrieved.transfer_amount), float(self.transfer.transfer_amount), places=2)

    def test_delete_transfer(self):
        transfer_to_delete = Transfer(
            account_id_from=self.account_from.account_id,
            account_id_to=self.account_to.account_id,
            transfer_amount=999.99
        )
        transfer_to_delete.save_to_db()
        deleted = transfer_to_delete.delete_transfer()
        self.assertTrue(deleted)
        self.assertIsNone(Transfer.get_by_id(transfer_to_delete.transfer_id))

if __name__ == "__main__":
    unittest.main()
