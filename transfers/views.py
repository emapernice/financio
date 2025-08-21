from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import Transfer
from .forms import TransferForm


@login_required
def transfer_list(request):
    transfers = Transfer.objects.filter(from_account__user=request.user) | Transfer.objects.filter(to_account__user=request.user)
    transfers = transfers.distinct().order_by('-created_at')
    return render(request, 'transfers/transfer_list.html', {'transfers': transfers})


@login_required
def transfer_create(request):
    if request.method == 'POST':
        form = TransferForm(request.POST, user=request.user)  
        if form.is_valid():
            transfer = form.save()
            messages.success(request, "Transfer created successfully.")
            return redirect('transfers:transfer_list')
    else:
        form = TransferForm(user=request.user)  
    return render(request, 'transfers/transfer_form.html', {'form': form})


@login_required
def transfer_update(request, pk):
    transfer = get_object_or_404(Transfer, pk=pk)
    if request.method == 'POST':
        form = TransferForm(request.POST, instance=transfer, user=request.user)  
        if form.is_valid():
            form.save()
            messages.success(request, "Transfer updated successfully.")
            return redirect('transfers:transfer_list')
    else:
        form = TransferForm(instance=transfer, user=request.user)  
    return render(request, 'transfers/transfer_form.html', {'form': form})


@login_required
def transfer_delete(request, pk):
    transfer = get_object_or_404(Transfer, pk=pk)
    if request.method == 'POST':
        transfer.delete()
        messages.success(request, "Transfer deleted successfully.")
        return redirect('transfers:transfer_list')
    return render(request, 'transfers/transfer_confirm_delete.html', {'transfer': transfer})
