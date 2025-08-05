from django.contrib import admin
from .models import Investment


@admin.register(Investment)
class InvestmentAdmin(admin.ModelAdmin):
    list_display = (
        'account',
        'amount',
        'interest_rate',
        'start_date',
        'end_date',
        'status',
        'expected_interest_display',
    )
    list_filter = (
        'status',
        'account',
        'start_date',
        'end_date',
    )
    search_fields = (
        'account__account_name',
        'description',
    )
    date_hierarchy = 'start_date'
    ordering = ('-start_date',)

    def expected_interest_display(self, obj):
        return f"{obj.expected_interest:.2f}"
    expected_interest_display.short_description = 'Expected Interest'
