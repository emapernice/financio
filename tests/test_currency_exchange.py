import unittest
from models.currency_exchange import CurrencyExchange
from models.currency import Currency  
from datetime import datetime

class TestCurrencyExchangeModel(unittest.TestCase):
    def setUp(self):
        self.ars = Currency.get_by_code("ARS")
        if not self.ars:
            self.ars = Currency("ARS", "Argentine peso")
            self.ars.save_to_db()

        self.usd = Currency.get_by_code("USD")
        if not self.usd:
            self.usd = Currency("USD", "US dollar")
            self.usd.save_to_db()

        self.exchange = CurrencyExchange(
            from_currency_id=self.ars.currency_id,
            to_currency_id=self.usd.currency_id,
            exchange_rate=1000.123456,
            exchange_date=datetime(2024, 5, 20)
        )
        self.exchange.save_to_db()

    def test_insert_and_get_exchange(self):
        retrieved = CurrencyExchange.get_by_id(self.exchange.exchange_id)
        self.assertIsNotNone(retrieved)
        self.assertAlmostEqual(float(retrieved.exchange_rate), float(self.exchange.exchange_rate), places=6)
        self.assertEqual(retrieved.from_currency_id, self.ars.currency_id)
        self.assertEqual(retrieved.to_currency_id, self.usd.currency_id)

    def test_delete_exchange(self):
        exchange_to_delete = CurrencyExchange(
            from_currency_id=self.ars.currency_id,
            to_currency_id=self.usd.currency_id,
            exchange_rate=999.99
        )
        exchange_to_delete.save_to_db()
        deleted = exchange_to_delete.delete_exchange()
        self.assertTrue(deleted)
        self.assertIsNone(CurrencyExchange.get_by_id(exchange_to_delete.exchange_id))

if __name__ == "__main__":
    unittest.main()
