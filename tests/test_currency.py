import unittest
from models.currency import Currency

class TestCurrencyModel(unittest.TestCase):
    def setUp(self):
        self.currency_code = "USD"
        existing = Currency.get_by_code(self.currency_code)
        if existing:
            existing.delete_currency()

        self.currency = Currency(currency_code=self.currency_code, currency_name="US Dollar")
        self.currency.save_to_db()

    def test_currency_insertion_and_duplicate(self):
        duplicate = Currency(currency_code=self.currency_code, currency_name="Duplicate Dollar")
        result = duplicate.save_to_db()
        self.assertFalse(result, "Should not allow duplicate currency codes")

    def test_get_by_id_and_code(self):
        currency_by_code = Currency.get_by_code(self.currency_code)
        self.assertIsNotNone(currency_by_code)
        self.assertEqual(currency_by_code.currency_code, self.currency_code)

        currency_by_id = Currency.get_by_id(currency_by_code.currency_id)
        self.assertIsNotNone(currency_by_id)
        self.assertEqual(currency_by_id.currency_id, currency_by_code.currency_id)

    def test_update_currency(self):
        currency = Currency.get_by_code("USD")
        updated = currency.update_currency(new_name="American Dollar")
        self.assertTrue(updated)
        updated_currency = Currency.get_by_code("USD")
        self.assertEqual(updated_currency.currency_name, "American Dollar")

    def test_delete_currency(self):
        temp_currency = Currency(currency_code="DEL", currency_name="To Delete")
        temp_currency.save_to_db()
        currency = Currency.get_by_code("DEL")
        result = currency.delete_currency()
        self.assertTrue(result)
        deleted = Currency.get_by_code("DEL")
        self.assertIsNone(deleted)

if __name__ == "__main__":
    unittest.main()