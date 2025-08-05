from django.contrib import admin
from .models import Currency, Entity, CurrencyExchange, DailyExchangeRate


@admin.register(Currency)
class CurrencyAdmin(admin.ModelAdmin):
    list_display = ('currency_code', 'currency_name')
    search_fields = ('currency_code', 'currency_name')
    ordering = ('currency_code',)


@admin.register(Entity)
class EntityAdmin(admin.ModelAdmin):
    list_display = ('entity_name', 'entity_type', 'entity_description')
    list_filter = ('entity_type',)
    search_fields = ('entity_name', 'entity_description')
    ordering = ('entity_type', 'entity_name')


@admin.register(CurrencyExchange)
class CurrencyExchangeAdmin(admin.ModelAdmin):
    list_display = ('from_currency', 'to_currency', 'exchange_rate', 'exchange_date')
    list_filter = ('from_currency', 'to_currency', 'exchange_date')
    search_fields = (
        'from_currency__currency_code',
        'to_currency__currency_code',
    )
    ordering = ('-exchange_date',)
    date_hierarchy = 'exchange_date'


@admin.register(DailyExchangeRate)
class DailyExchangeRateAdmin(admin.ModelAdmin):
    list_display = ('currency', 'base_currency', 'rate_against_base', 'date')
    list_filter = ('currency', 'base_currency', 'date')
    search_fields = (
        'currency__currency_code',
        'base_currency__currency_code',
    )
    ordering = ('-date',)
    date_hierarchy = 'date'
