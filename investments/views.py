from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import Investment
from .forms import InvestmentForm
from .services import create_investment_outflow, create_investment_inflow


@login_required
def investment_list(request):
    investments = Investment.objects.filter(account__user=request.user)
    return render(request, 'investments/investment_list.html', {'investments': investments})


@login_required
def investment_create(request):
    if request.method == 'POST':
        form = InvestmentForm(request.POST)
        if form.is_valid():
            investment = form.save(commit=False)
            if investment.account.user != request.user:
                messages.error(request, "You cannot assign investments to accounts that are not yours.")
                return redirect('investments:investment_list')
            investment.save()

            create_investment_outflow(investment, request.user)

            messages.success(request, "Investment created successfully.")
            return redirect('investments:investment_list')
    else:
        form = InvestmentForm()
    return render(request, 'investments/investment_form.html', {'form': form})


@login_required
def investment_update(request, pk):
    investment = get_object_or_404(Investment, pk=pk, account__user=request.user)
    old_status = investment.status
    if request.method == 'POST':
        form = InvestmentForm(request.POST, instance=investment)
        if form.is_valid():
            investment = form.save()

            if old_status == "active" and investment.status == "closed" and not investment.inflow_record:
                create_investment_inflow(investment, request.user)

            messages.success(request, "Investment updated successfully.")
            return redirect('investments:investment_list')
    else:
        form = InvestmentForm(instance=investment)
    return render(request, 'investments/investment_form.html', {'form': form})


@login_required
def investment_delete(request, pk):
    investment = get_object_or_404(Investment, pk=pk, account__user=request.user)
    if request.method == 'POST':
        if investment.outflow_record or investment.inflow_record:
            messages.error(
                request,
                "Cannot delete investment with associated records. Mark it as cancelled instead."
            )
            return redirect('investments:investment_list')

        investment.delete()
        messages.success(request, "Investment deleted successfully.")
        return redirect('investments:investment_list')
    return render(request, 'investments/investment_confirm_delete.html', {'investment': investment})
