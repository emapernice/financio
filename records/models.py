from django.db import models
from accounts.models import Account
from core.models import Currency, Entity


class Category(models.Model):
    CATEGORY_TYPES = [
        ('income', 'Income'),
        ('expense', 'Expense'),
        ('transfer', 'Transfer'),
    ]

    category_name = models.CharField(max_length=100)
    category_type = models.CharField(max_length=20, choices=CATEGORY_TYPES)

    class Meta:
        unique_together = ('category_name', 'category_type')

    def __str__(self):
        return self.category_name


class Subcategory(models.Model):
    category = models.ForeignKey(
        Category, on_delete=models.CASCADE, related_name='subcategories'
    )
    subcategory_name = models.CharField(max_length=100)
    is_fixed = models.BooleanField(default=False)

    class Meta:
        unique_together = ('category', 'subcategory_name')

    def __str__(self):
        return f"{self.category.category_name} - {self.subcategory_name}"


class Record(models.Model):
    RECORD_TYPES = [
        ('income', 'Income'),
        ('expense', 'Expense'),
        ('transfer', 'Transfer'),
    ]

    record_type = models.CharField(max_length=10, choices=RECORD_TYPES)
    account = models.ForeignKey(
        Account, on_delete=models.CASCADE, related_name='records'
    )
    transfer_account = models.ForeignKey(
        Account, on_delete=models.CASCADE, null=True, blank=True, related_name='transfer_records'
    )
    record_amount = models.DecimalField(max_digits=12, decimal_places=2)
    currency = models.ForeignKey(Currency, on_delete=models.PROTECT)
    entity = models.ForeignKey(Entity, on_delete=models.PROTECT, null=True, blank=True)

    subcategory = models.ForeignKey(
        Subcategory, on_delete=models.SET_NULL, null=True, blank=True, related_name='records'
    )
    record_description = models.TextField(blank=True)
    record_date = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)

    def clean(self):
        from django.core.exceptions import ValidationError

        if self.record_type == 'transfer' and not self.transfer_account:
            raise ValidationError('Transfer records must have a transfer_account.')
        if self.record_type != 'transfer' and self.transfer_account:
            raise ValidationError('Only transfer records can have a transfer_account.')

    def __str__(self):
        return f"{self.record_type.title()} - {self.record_amount} on {self.record_date}"
