from django.contrib import admin
from .models import FixedRecord


@admin.register(FixedRecord)
class FixedRecordAdmin(admin.ModelAdmin):
    list_display = (
        'record_type',
        'amount',
        'account',
        'subcategory',
        'frequency',
        'start_date',
        'end_date',
        'next_execution',
        'is_active',
    )
    list_filter = (
        'record_type',
        'frequency',
        'is_active',
        'account',
        'subcategory',
    )
    search_fields = (
        'account__account_name',
        'subcategory__subcategory_name',
    )
    date_hierarchy = 'next_execution'
    ordering = ('next_execution',)
    list_editable = ('is_active',)
