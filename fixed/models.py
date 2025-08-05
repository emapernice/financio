from django.db import models
from accounts.models import Account
from records.models import Subcategory


class FixedRecord(models.Model):
    RECORD_TYPES = [
        ('income', 'Income'),
        ('expense', 'Expense'),
    ]

    FREQUENCIES = [
        ('daily', 'Daily'),
        ('weekly', 'Weekly'),
        ('monthly', 'Monthly'),
        ('yearly', 'Yearly'),
    ]

    account = models.ForeignKey(
        Account, on_delete=models.CASCADE, related_name='fixed_records'
    )
    subcategory = models.ForeignKey(
        Subcategory, on_delete=models.SET_NULL, null=True, blank=True, related_name='fixed_records'
    )
    record_type = models.CharField(max_length=10, choices=RECORD_TYPES)
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    frequency = models.CharField(max_length=10, choices=FREQUENCIES)
    start_date = models.DateField()
    end_date = models.DateField(null=True, blank=True)
    next_execution = models.DateField()
    is_active = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['next_execution']
        verbose_name = "Fixed Record"
        verbose_name_plural = "Fixed Records"

    def __str__(self):
        return f"{self.get_record_type_display()} - {self.amount} every {self.frequency}"
