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
            'transfer_date',
        ]
        widgets = {
            'from_account': forms.Select(attrs={
                'class': 'form-select',
                'id': 'id_from_account'
            }),
            'to_account': forms.Select(attrs={
                'class': 'form-select',
                'id': 'id_to_account'
            }),
            'transfer_amount': forms.NumberInput(attrs={
                'class': 'form-control',
                'step': '0.01'
            }),
            'transfer_description': forms.TextInput(attrs={
                'class': 'form-control'
            }),
            'currency': forms.HiddenInput(),
            'transfer_date': forms.DateInput(attrs={
                'type': 'date',
                'class': 'form-control'
            }),
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)

        if user:
            accounts = Account.objects.filter(user=user)
            self.fields['from_account'].queryset = accounts
            self.fields['to_account'].queryset = accounts

    def clean(self):
        cleaned_data = super().clean()
        from_account = cleaned_data.get("from_account")
        to_account = cleaned_data.get("to_account")

        if from_account and to_account:
            if from_account == to_account:
                self.add_error('to_account', "The destination account cannot be the same as the source account.")
            elif from_account.currency != to_account.currency:
                self.add_error('to_account', "The destination account must have the same currency as the source account.")

        if from_account:
            cleaned_data['currency'] = from_account.currency

        return cleaned_data
