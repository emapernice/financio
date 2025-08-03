from django.db import models

class Currency(models.Model):
    currency_name = models.CharField(max_length=50, unique=True)        # Ej: Dólar estadounidense
    currency_code = models.CharField(max_length=3, unique=True)         # Ej: USD, ARS

    def __str__(self):
        return f"{self.currency_code} - {self.currency_name}"


class Entity(models.Model):
    ENTITY_TYPES = [
        ('SUPPLIER', 'Proveedor'),
        ('INCOME_SOURCE', 'Fuente de ingreso'),
    ]

    entity_name = models.CharField(max_length=100)
    entity_description = models.TextField(blank=True)
    entity_type = models.CharField(max_length=20, choices=ENTITY_TYPES)

    def __str__(self):
        return f"{self.entity_name} ({self.get_entity_type_display()})"


class CurrencyExchange(models.Model):
    from_currency = models.ForeignKey(Currency, on_delete=models.CASCADE, related_name='from_currency_exchanges')
    to_currency = models.ForeignKey(Currency, on_delete=models.CASCADE, related_name='to_currency_exchanges')
    exchange_rate = models.DecimalField(max_digits=12, decimal_places=6) 
    exchange_date = models.DateField()

    class Meta:
        unique_together = ('from_currency', 'to_currency', 'exchange_date')

    def __str__(self):
        return f"{self.from_currency.currency_code} → {self.to_currency.currency_code} @ {self.exchange_rate} on {self.exchange_date}"


class DailyExchangeRate(models.Model):
    currency = models.ForeignKey(Currency, on_delete=models.CASCADE)
    rate_against_base = models.DecimalField(max_digits=12, decimal_places=6)
    base_currency = models.ForeignKey(Currency, on_delete=models.CASCADE, related_name='base_currency_rates')
    date = models.DateField()

    class Meta:
        unique_together = ('currency', 'base_currency', 'date')

    def __str__(self):
        return f"{self.currency.currency_code} vs {self.base_currency.currency_code} = {self.rate_against_base} ({self.date})"
