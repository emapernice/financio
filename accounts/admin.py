from django.contrib import admin
from .models import Account, Transfer


@admin.register(Account)
class AccountAdmin(admin.ModelAdmin):
    list_display = ('account_name', 'user', 'account_type', 'currency', 'initial_balance', 'created_at')
    list_filter = ('account_type', 'currency', 'user')
    search_fields = ('account_name', 'user__username')
    ordering = ('-created_at',)


@admin.register(Transfer)
class TransferAdmin(admin.ModelAdmin):
    list_display = ('from_account', 'to_account', 'transfer_amount', 'transfer_description', 'created_at')
    list_filter = ('from_account__currency',)
    search_fields = (
        'from_account__account_name',
        'to_account__account_name',
        'transfer_description'
    )
    ordering = ('-created_at',)
