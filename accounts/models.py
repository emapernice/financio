from django.db import models
from django.conf import settings


class Account(models.Model):
    ACCOUNT_TYPES = [
        ('cash', 'Cash'),
        ('bank', 'Bank'),
        ('credit', 'Credit Card'),
        ('other', 'Other'),
    ]

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='accounts'
    )
    account_name = models.CharField(max_length=100)
    account_type = models.CharField(max_length=20, choices=ACCOUNT_TYPES)
    currency = models.ForeignKey(
        "core.Currency", on_delete=models.PROTECT, related_name='accounts'
    )
    initial_balance = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['user', 'account_name'], name='unique_account_per_user'),
        ]
        ordering = ["account_name"]

    def clean(self):
        from django.core.exceptions import ValidationError

        if self.initial_balance < 0:
            raise ValidationError("Initial balance cannot be negative.")

    def __str__(self):
        return f"{self.account_name} [{self.get_account_type_display()}] {self.currency.currency_code}"
