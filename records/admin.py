from django.contrib import admin
from .models import Category, Subcategory, Record
from core.models import Entity


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('category_name', 'category_type')
    list_filter = ('category_type',)
    search_fields = ('category_name',)


@admin.register(Subcategory)
class SubcategoryAdmin(admin.ModelAdmin):
    list_display = ('subcategory_name', 'category', 'is_fixed')
    list_filter = ('category', 'is_fixed')
    search_fields = ('subcategory_name',)


@admin.register(Record)
class RecordAdmin(admin.ModelAdmin):
    list_display = ('record_type', 'record_amount', 'account', 'currency', 'entity', 'record_date', 'created_at')
    list_filter = ('record_type', 'currency', 'record_date')
    search_fields = ('record_description',)
    date_hierarchy = 'record_date'
    ordering = ('-record_date',)
