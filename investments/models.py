from django.db import models
from accounts.models import Account


class Investment(models.Model):
    STATUS_CHOICES = [
        ('active', 'Active'),
        ('closed', 'Closed'),
        ('cancelled', 'Cancelled'),
    ]

    account = models.ForeignKey(
        Account, on_delete=models.CASCADE, related_name='investments'
    )
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    interest_rate = models.DecimalField(
        max_digits=5, decimal_places=2, help_text="Annual interest rate in %"
    )
    start_date = models.DateField()
    end_date = models.DateField()
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='active')
    description = models.CharField(max_length=255, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-start_date']
        verbose_name = 'Investment'
        verbose_name_plural = 'Investments'

    def __str__(self):
        return f"Investment of {self.amount} from {self.start_date} to {self.end_date} ({self.status})"

    @property
    def expected_interest(self):
        """Calculate interest based on annual rate and period in days."""
        total_days = (self.end_date - self.start_date).days
        return (self.amount * self.interest_rate * total_days) / (100 * 365)
