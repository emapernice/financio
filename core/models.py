from django.db import models
from django.core.exceptions import ValidationError
from django.apps import apps
from django.utils import timezone


class Currency(models.Model):
    currency_name = models.CharField(max_length=50, unique=True)
    currency_code = models.CharField(max_length=3, unique=True)

    def __str__(self):
        return f"{self.currency_code} - {self.currency_name}"


class Entity(models.Model):
    ENTITY_TYPES = [
        ('SUPPLIER', 'Supplier'),
        ('INCOME_SOURCE', 'Source of income'),
    ]

    entity_name = models.CharField(max_length=100)
    entity_description = models.TextField(blank=True)
    entity_type = models.CharField(
        max_length=20,
        choices=ENTITY_TYPES,
        blank=False,
        null=False,
        default='SUPPLIER'
    )

    def __str__(self):
        return f"{self.entity_name} ({self.get_entity_type_display()})"


class CurrencyExchange(models.Model):
    from_account = models.ForeignKey(
        "accounts.Account", on_delete=models.CASCADE, related_name='currency_exchanges_out'
    )
    to_account = models.ForeignKey(
        "accounts.Account", on_delete=models.CASCADE, related_name='currency_exchanges_in'
    )
    from_currency = models.ForeignKey(
        "core.Currency", on_delete=models.CASCADE, related_name='currency_exchanges_from'
    )
    to_currency = models.ForeignKey(
        "core.Currency", on_delete=models.CASCADE, related_name='currency_exchanges_to'
    )
    from_amount = models.DecimalField(max_digits=12, decimal_places=2)
    to_amount = models.DecimalField(max_digits=12, decimal_places=2)
    exchange_rate = models.DecimalField(max_digits=12, decimal_places=6)
    exchange_date = models.DateField(default=timezone.now)
    created_at = models.DateTimeField(default=timezone.now, editable=False)
    description = models.CharField(max_length=255, blank=True)

    class Meta:
        ordering = ["-exchange_date", "-created_at"]

    def clean(self):
        super().clean()

        if self.from_account == self.to_account:
            raise ValidationError("From account and To account must be different.")

        if self.from_currency == self.to_currency:
            raise ValidationError("From currency and To currency must be different.")

        if self.from_amount <= 0:
            raise ValidationError("From amount must be greater than zero.")

        if self.to_amount <= 0:
            raise ValidationError("To amount must be greater than zero.")

        if self.exchange_rate <= 0:
            raise ValidationError("Exchange rate must be greater than zero.")

        

    def save(self, *args, **kwargs):
        creating = self.pk is None
        self.clean()
        super().save(*args, **kwargs)

        if creating:
            self._create_records()
        else:
            self._update_records()

    def delete(self, *args, **kwargs):
        self.records.all().delete()
        super().delete(*args, **kwargs)

    def _get_or_create_categories(self):
        Category = apps.get_model('records', 'Category')
        Subcategory = apps.get_model('records', 'Subcategory')

        expense_cat, _ = Category.objects.get_or_create(
            category_name="Exchange", category_type="expense"
        )
        income_cat, _ = Category.objects.get_or_create(
            category_name="Exchange", category_type="income"
        )
        expense_sub, _ = Subcategory.objects.get_or_create(
            category=expense_cat, subcategory_name=f"{self.from_currency.currency_code} out"
        )
        income_sub, _ = Subcategory.objects.get_or_create(
            category=income_cat, subcategory_name=f"{self.to_currency.currency_code} in"
        )
        return expense_sub, income_sub

    def _create_records(self):
        Record = apps.get_model('records', 'Record')
        expense_sub, income_sub = self._get_or_create_categories()

        Record.objects.create(
            record_type="expense",
            account=self.from_account,
            record_amount=self.from_amount,
            currency=self.from_currency,
            subcategory=expense_sub,
            record_description=self.description or f"Exchange {self.from_currency} → {self.to_currency}",
            record_date=self.exchange_date,
            exchange=self,
        )

        Record.objects.create(
            record_type="income",
            account=self.to_account,
            record_amount=self.to_amount,
            currency=self.to_currency,
            subcategory=income_sub,
            record_description=self.description or f"Exchange {self.from_currency} → {self.to_currency}",
            record_date=self.exchange_date,
            exchange=self,
        )

    def _update_records(self):
        expense_sub, income_sub = self._get_or_create_categories()

        for record in self.records.all():
            if record.record_type == "expense":
                record.account = self.from_account
                record.record_amount = self.from_amount
                record.currency = self.from_currency
                record.subcategory = expense_sub
                record.record_description = self.description or f"Exchange {self.from_currency} → {self.to_currency}"
                record.record_date = self.exchange_date
                record.exchange = self
                record.save()

            elif record.record_type == "income":
                record.account = self.to_account
                record.record_amount = self.to_amount
                record.currency = self.to_currency
                record.subcategory = income_sub
                record.record_description = self.description or f"Exchange {self.from_currency} → {self.to_currency}"
                record.record_date = self.exchange_date
                record.exchange = self
                record.save()

    def __str__(self):
        return f"{self.from_amount} {self.from_currency.currency_code} → {self.to_amount} {self.to_currency.currency_code} @ {self.exchange_rate}"


class DailyExchangeRate(models.Model):
    currency = models.ForeignKey(Currency, on_delete=models.CASCADE)
    rate_against_base = models.DecimalField(max_digits=12, decimal_places=6)
    base_currency = models.ForeignKey(
        Currency, on_delete=models.CASCADE, related_name='base_currency_rates'
    )
    date = models.DateField()

    class Meta:
        unique_together = ('currency', 'base_currency', 'date')

    def __str__(self):
        return f"{self.currency.currency_code} vs {self.base_currency.currency_code} = {self.rate_against_base} ({self.date})"
