from django.db import models
from django.conf import settings
from accounts.models import Account
from core.models import Currency, Entity, CurrencyExchange


class Category(models.Model):
    CATEGORY_TYPES = [
        ('income', 'Income'),
        ('expense', 'Expense'),
    ]

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="categories",
        null=True,
        blank=True,
        help_text="Null = global category, not tied to a specific user",
    )
    category_name = models.CharField(max_length=100)
    category_type = models.CharField(max_length=20, choices=CATEGORY_TYPES)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'category_name', 'category_type'],
                name='unique_category_per_user_or_global',
            ),
        ]

    def __str__(self):
        scope = "Global" if self.user is None else f"User {self.user.username}"
        return f"{self.category_name} ({self.category_type}) [{scope}]"


class Subcategory(models.Model):
    category = models.ForeignKey(
        Category, on_delete=models.CASCADE, related_name='subcategories'
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="subcategories",
        null=True,
        blank=True,
        help_text="Null = global subcategory, not tied to a specific user",
    )
    subcategory_name = models.CharField(max_length=100)
    is_fixed = models.BooleanField(default=False)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['category', 'user', 'subcategory_name'],
                name='unique_subcategory_per_category_user_or_global',
            ),
        ]

    def __str__(self):
        scope = "Global" if self.user is None else f"User {self.user.username}"
        return f"{self.category.category_name} - {self.subcategory_name} [{scope}]"


class Record(models.Model):
    RECORD_TYPES = [
        ('income', 'Income'),
        ('expense', 'Expense'),
    ]

    record_type = models.CharField(max_length=10, choices=RECORD_TYPES)
    account = models.ForeignKey(
        Account, on_delete=models.CASCADE, related_name='records'
    )
    
    transfer = models.ForeignKey(
        "transfers.Transfer", on_delete=models.CASCADE, null=True, blank=True, related_name="records"
    )
    transfer_account = models.ForeignKey(
        Account, on_delete=models.CASCADE, null=True, blank=True, related_name='records_as_transfer_account'
    )

    exchange = models.ForeignKey(
        CurrencyExchange, on_delete=models.CASCADE, null=True, blank=True, related_name="records"
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

    class Meta:
        ordering = ["-record_date", "-created_at"]

    def clean(self):
        from django.core.exceptions import ValidationError

        if self.transfer and not self.transfer_account:
            raise ValidationError("Transfer records must always have a transfer_account.")

        if not self.transfer and self.transfer_account:
            raise ValidationError("Non-transfer records cannot have a transfer_account.")

        if self.transfer and self.exchange:
            raise ValidationError("A record cannot belong to both a transfer and an exchange.")

    def __str__(self):
        return (
            f"{self.record_type.title()} {self.record_amount} {self.currency.currency_code} "
            f"({self.account}) on {self.record_date}"
        )
