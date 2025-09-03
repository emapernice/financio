from django import forms
from .models import Currency, Entity, CurrencyExchange


class CurrencyForm(forms.ModelForm):
    class Meta:
        model = Currency
        fields = ['currency_name', 'currency_code']
        widgets = {
            'currency_name': forms.TextInput(attrs={'class': 'form-control'}),
            'currency_code': forms.TextInput(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'


class EntityForm(forms.ModelForm):
    class Meta:
        model = Entity
        fields = ['entity_name', 'entity_description', 'entity_type']
        widgets = {
            'entity_name': forms.TextInput(attrs={'class': 'form-control'}),
            'entity_description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'entity_type': forms.Select(attrs={'class': 'form-select'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            if field_name != 'entity_type':
                field.widget.attrs['class'] = 'form-control'


class CurrencyExchangeForm(forms.ModelForm):
    class Meta:
        model = CurrencyExchange
        fields = [
            'from_account',
            'to_account',
            'from_currency',
            'to_currency',
            'from_amount',
            'to_amount',
            'exchange_rate',
            'exchange_date',
            'description',
        ]
        widgets = {
            'from_account': forms.Select(attrs={'class': 'form-select'}),
            'to_account': forms.Select(attrs={'class': 'form-select'}),
            'from_currency': forms.Select(attrs={'class': 'form-select'}),
            'to_currency': forms.Select(attrs={'class': 'form-select'}),
            'from_amount': forms.NumberInput(attrs={'class': 'form-control'}),
            'to_amount': forms.NumberInput(attrs={'class': 'form-control'}),
            'exchange_rate': forms.NumberInput(attrs={'class': 'form-control'}),
            'exchange_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'description': forms.TextInput(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            if not isinstance(field.widget, forms.Select):
                field.widget.attrs['class'] = 'form-control'

