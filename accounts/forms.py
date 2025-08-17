from django import forms
from .models import Account, Transfer

class AccountForm(forms.ModelForm):
    class Meta:
        model = Account
        fields = ['account_name', 'account_type', 'currency', 'initial_balance']
        widgets = {
            'account_name': forms.TextInput(attrs={'class': 'form-control'}),
            'account_type': forms.Select(attrs={'class': 'form-control'}),
            'currency': forms.Select(attrs={'class': 'form-control'}),
            'initial_balance': forms.NumberInput(attrs={'step': '0.01', 'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'


class TransferForm(forms.ModelForm):
    class Meta:
        model = Transfer
        fields = ['from_account', 'to_account', 'transfer_amount', 'transfer_description']
        widgets = {
            'from_account': forms.Select(attrs={'class': 'form-control'}),
            'to_account': forms.Select(attrs={'class': 'form-control'}),
            'transfer_amount': forms.NumberInput(attrs={'step': '0.01', 'class': 'form-control'}),
            'transfer_description': forms.TextInput(attrs={'class': 'form-control'}),
        }

    def __init__(self, user, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['from_account'].queryset = Account.objects.filter(user=user)
        self.fields['to_account'].queryset = Account.objects.filter(user=user)
