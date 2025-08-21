from django.contrib import admin
from .models import Account


@admin.register(Account)
class AccountAdmin(admin.ModelAdmin):
    list_display = ('account_name', 'user', 'account_type', 'currency', 'initial_balance', 'created_at')
    list_filter = ('account_type', 'currency', 'user')
    search_fields = ('account_name', 'user__username')
    ordering = ('-created_at',)
