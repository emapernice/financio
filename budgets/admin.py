from django.contrib import admin
from .models import Budget


@admin.register(Budget)
class BudgetAdmin(admin.ModelAdmin):
    list_display = (
        'user',
        'subcategory',
        'amount',
        'currency',
        'period_start',
        'period_end',
        'is_active',
    )
    list_filter = (
        'user',
        'subcategory',
        'currency',
        'is_active',
    )
    search_fields = (
        'user__username',
        'subcategory__subcategory_name',
    )
    date_hierarchy = 'period_start'
    ordering = ('-period_start',)
    list_editable = ('is_active',)
