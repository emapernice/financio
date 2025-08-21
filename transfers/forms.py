from django import forms
from .models import Transfer
from accounts.models import Account


class TransferForm(forms.ModelForm):
    class Meta:
        model = Transfer
        fields = [
            'from_account',
            'to_account',
            'transfer_amount',
            'transfer_description',
            'currency',
        ]
        widgets = {
            'from_account': forms.Select(attrs={'class': 'form-select'}),
            'to_account': forms.Select(attrs={'class': 'form-select'}),
            'transfer_amount': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'transfer_description': forms.TextInput(attrs={'class': 'form-control'}),
            'currency': forms.Select(attrs={'class': 'form-select'}),
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)  
        super().__init__(*args, **kwargs)

        if user is not None:
            self.fields['from_account'].queryset = Account.objects.filter(user=user)
            self.fields['to_account'].queryset = Account.objects.filter(user=user)

        for field_name, field in self.fields.items():
            if isinstance(field.widget, forms.Select):
                field.widget.attrs['class'] = 'form-select'
            elif isinstance(field.widget, forms.CheckboxInput):
                field.widget.attrs['class'] = 'form-check-input'
            else:
                field.widget.attrs['class'] = 'form-control'
