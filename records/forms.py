from django import forms
from .models import Record, Category, Subcategory


class RecordForm(forms.ModelForm):
    class Meta:
        model = Record
        fields = [
            'record_type', 'account', 'transfer_account', 'record_amount', 'currency', 'entity',
            'subcategory', 'record_description', 'record_date'
        ]
        widgets = {
            'record_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'record_description': forms.Textarea(attrs={'rows': 3, 'class': 'form-control'}),
            'record_amount': forms.NumberInput(attrs={'step': '0.01', 'class': 'form-control'}),
            'transfer_account': forms.Select(attrs={'class': 'form-control'}),
            'account': forms.Select(attrs={'class': 'form-control'}),
            'currency': forms.Select(attrs={'class': 'form-control'}),
            'entity': forms.Select(attrs={'class': 'form-control'}),
            'subcategory': forms.Select(attrs={'class': 'form-control'}),
            'record_type': forms.Select(attrs={'class': 'form-control'}),
        }


class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['category_name', 'category_type']
        widgets = {
            'category_name': forms.TextInput(attrs={'class': 'form-control'}),
            'category_type': forms.Select(attrs={'class': 'form-control'}),
        }


class SubcategoryForm(forms.ModelForm):
    class Meta:
        model = Subcategory
        fields = ['category', 'subcategory_name', 'is_fixed']
        widgets = {
            'category': forms.Select(attrs={'class': 'form-control'}),
            'subcategory_name': forms.TextInput(attrs={'class': 'form-control'}),
            'is_fixed': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }
