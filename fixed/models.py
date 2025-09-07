from datetime import timedelta

from django.db import models
from django.db.models import Q, F
from accounts.models import Account
from records.models import Subcategory
from dateutil.relativedelta import relativedelta


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

    next_execution = models.DateField(db_index=True)

    is_active = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['next_execution']
        verbose_name = "Fixed Record"
        verbose_name_plural = "Fixed Records"
        constraints = [
            models.CheckConstraint(
                check=Q(amount__gt=0),
                name='fixed_amount_gt_0',
            ),
            models.CheckConstraint(
                check=Q(end_date__isnull=True) | Q(end_date__gte=F('start_date')),
                name='fixed_end_gte_start',
            ),
            models.CheckConstraint(
                check=Q(next_execution__gte=F('start_date')),
                name='fixed_next_gte_start',
            ),
        ]
        indexes = [
            models.Index(fields=['is_active', 'next_execution'], name='fixed_active_next_idx'),
        ]

    def __str__(self):
        curr = getattr(self.account.currency, 'currency_code', str(self.account.currency))
        return f"{self.get_record_type_display()} - {self.amount} {curr} every {self.frequency}"

    def update_next_execution(self):
        if self.frequency == "daily":
            self.next_execution += timedelta(days=1)
        elif self.frequency == "weekly":
            self.next_execution += timedelta(weeks=1)
        elif self.frequency == "monthly":
            self.next_execution += relativedelta(months=1)
        elif self.frequency == "yearly":
            self.next_execution += relativedelta(years=1)

        if self.end_date and self.next_execution > self.end_date:
            self.is_active = False
            self.save(update_fields=["next_execution", "is_active"])
        else:
            self.save(update_fields=["next_execution"])
