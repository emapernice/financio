from django.db import models
from django.conf import settings
from records.models import Subcategory
from core.models import Currency


class Budget(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='budgets'
    )
    subcategory = models.ForeignKey(
        Subcategory, on_delete=models.CASCADE, related_name='budgets'
    )
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    currency = models.ForeignKey(
        Currency, on_delete=models.PROTECT, related_name='budgets'
    )
    period_start = models.DateField()
    period_end = models.DateField()
    is_active = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-period_start']
        verbose_name = 'Budget'
        verbose_name_plural = 'Budgets'
        unique_together = ('user', 'subcategory', 'period_start', 'period_end')

    def __str__(self):
        return f"{self.subcategory} - {self.amount} {self.currency} ({self.period_start} to {self.period_end})"
