from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import Account
from .forms import AccountForm
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

