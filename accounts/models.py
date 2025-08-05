from django.db import models
from django.conf import settings
from django.core.exceptions import ValidationError
from core.models import Currency  


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
        Currency, on_delete=models.PROTECT, related_name='accounts'
    )
    initial_balance = models.DecimalField(max_digits=12, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.account_name} ({self.get_account_type_display()})"


class Transfer(models.Model):
    from_account = models.ForeignKey(
        Account, on_delete=models.CASCADE, related_name='transfers_out'
    )
    to_account = models.ForeignKey(
        Account, on_delete=models.CASCADE, related_name='transfers_in'
    )
    transfer_amount = models.DecimalField(max_digits=12, decimal_places=2)
    transfer_description = models.CharField(max_length=255, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def clean(self):
        if self.from_account == self.to_account:
            raise ValidationError("The source and destination accounts cannot be the same.")
        if self.transfer_amount <= 0:
            raise ValidationError("The transfer amount must be greater than zero.")

    def save(self, *args, **kwargs):
        self.clean()  
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.transfer_amount} from {self.from_account} to {self.to_account}"
