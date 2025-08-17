from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import Account, Transfer
from .forms import AccountForm, TransferForm
from django.contrib.auth.decorators import login_required

@login_required
def account_list(request):
    accounts = Account.objects.filter(user=request.user)
    return render(request, 'accounts/account_list.html', {'accounts': accounts})

@login_required
def account_detail(request, pk):
    account = get_object_or_404(Account, pk=pk, user=request.user)
    return render(request, 'accounts/account_detail.html', {'account': account})

@login_required
def account_create(request):
    if request.method == 'POST':
        form = AccountForm(request.POST)
        if form.is_valid():
            account = form.save(commit=False)
            account.user = request.user
            account.save()
            messages.success(request, "Cuenta creada correctamente.")
            return redirect('accounts:account_list')
    else:
        form = AccountForm()
    return render(request, 'accounts/account_form.html', {'form': form})

@login_required
def account_update(request, pk):
    account = get_object_or_404(Account, pk=pk, user=request.user)
    if request.method == 'POST':
        form = AccountForm(request.POST, instance=account)
        if form.is_valid():
            form.save()
            messages.success(request, "Cuenta actualizada correctamente.")
            return redirect('accounts:account_list')
    else:
        form = AccountForm(instance=account)
    return render(request, 'accounts/account_form.html', {'form': form})

@login_required
def account_delete(request, pk):
    account = get_object_or_404(Account, pk=pk, user=request.user)
    if request.method == 'POST':
        account.delete()
        messages.success(request, "Cuenta eliminada correctamente.")
        return redirect('accounts:account_list')
    return render(request, 'accounts/account_confirm_delete.html', {'account': account})


@login_required
def transfer_list(request):
    transfers = Transfer.objects.filter(from_account__user=request.user)
    return render(request, 'accounts/transfer_list.html', {'transfers': transfers})

@login_required
def transfer_detail(request, pk):
    transfer = get_object_or_404(Transfer, pk=pk, from_account__user=request.user)
    return render(request, 'accounts/transfer_detail.html', {'transfer': transfer})

@login_required
def transfer_create(request):
    if request.method == 'POST':
        form = TransferForm(request.user, request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Transferencia realizada correctamente.")
            return redirect('accounts:transfer_list')
    else:
        form = TransferForm(request.user)
    return render(request, 'accounts/transfer_form.html', {'form': form})

@login_required
def transfer_update(request, pk):
    transfer = get_object_or_404(Transfer, pk=pk, from_account__user=request.user)
    if request.method == 'POST':
        form = TransferForm(request.user, request.POST, instance=transfer)
        if form.is_valid():
            form.save()
            messages.success(request, "Transferencia actualizada correctamente.")
            return redirect('accounts:transfer_list')
    else:
        form = TransferForm(request.user, instance=transfer)
    return render(request, 'accounts/transfer_form.html', {'form': form})

@login_required
def transfer_delete(request, pk):
    transfer = get_object_or_404(Transfer, pk=pk, from_account__user=request.user)
    if request.method == 'POST':
        transfer.delete()
        messages.success(request, "Transferencia eliminada correctamente.")
        return redirect('accounts:transfer_list')
    return render(request, 'accounts/transfer_confirm_delete.html', {'transfer': transfer})
