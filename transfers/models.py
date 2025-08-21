from django.db import models
from django.core.exceptions import ValidationError
from django.apps import apps
from accounts.models import Account
from core.models import Currency
from django.utils import timezone


class Transfer(models.Model):
    from_account = models.ForeignKey(
        Account, on_delete=models.CASCADE, related_name='transfers_out'
    )
    to_account = models.ForeignKey(
        Account, on_delete=models.CASCADE, related_name='transfers_in'
    )
    transfer_amount = models.DecimalField(max_digits=12, decimal_places=2)
    transfer_description = models.CharField(max_length=255, blank=True)
    currency = models.ForeignKey(Currency, on_delete=models.PROTECT)
    transfer_date = models.DateField(default=timezone.now) 
    created_at = models.DateTimeField(auto_now_add=True)

    def clean(self):
        if self.from_account == self.to_account:
            raise ValidationError("The source and destination accounts cannot be the same.")
        if self.transfer_amount <= 0:
            raise ValidationError("The transfer amount must be greater than zero.")

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
            category_name="Transfer", category_type="expense"
        )
        income_cat, _ = Category.objects.get_or_create(
            category_name="Transfer", category_type="income"
        )
        expense_sub, _ = Subcategory.objects.get_or_create(
            category=expense_cat, subcategory_name="Transfer out"
        )
        income_sub, _ = Subcategory.objects.get_or_create(
            category=income_cat, subcategory_name="Transfer in"
        )
        return expense_sub, income_sub

    def _create_records(self):
        Record = apps.get_model('records', 'Record')
        expense_sub, income_sub = self._get_or_create_categories()

        Record.objects.create(
            transfer=self,
            record_type="expense",
            account=self.from_account,
            transfer_account=self.to_account,
            record_amount=self.transfer_amount,
            currency=self.currency,
            subcategory=expense_sub,
            record_description=self.transfer_description or f"Transfer to {self.to_account}",
            record_date=self.transfer_date,
        )

        Record.objects.create(
            transfer=self,
            record_type="income",
            account=self.to_account,
            transfer_account=self.from_account,
            record_amount=self.transfer_amount,
            currency=self.currency,
            subcategory=income_sub,
            record_description=self.transfer_description or f"Transfer from {self.from_account}",
            record_date=self.transfer_date,
        )

    def _update_records(self):
        expense_sub, income_sub = self._get_or_create_categories()

        for record in self.records.all():
            if record.record_type == "expense":
                record.account = self.from_account
                record.transfer_account = self.to_account
                record.record_amount = self.transfer_amount
                record.currency = self.currency
                record.subcategory = expense_sub
                record.record_description = self.transfer_description or f"Transfer to {self.to_account}"
                record.record_date = self.transfer_date
                record.save()

            elif record.record_type == "income":
                record.account = self.to_account
                record.transfer_account = self.from_account
                record.record_amount = self.transfer_amount
                record.currency = self.currency
                record.subcategory = income_sub
                record.record_description = self.transfer_description or f"Transfer from {self.from_account}"
                record.record_date = self.transfer_date
                record.save()

    def __str__(self):
        return f"{self.transfer_amount} from {self.from_account} to {self.to_account}"
