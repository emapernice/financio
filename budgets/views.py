from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import Budget
from .forms import BudgetForm


@login_required
def budget_list(request):
    budgets = Budget.objects.filter(user=request.user)
    return render(request, 'budgets/budget_list.html', {'budgets': budgets})


@login_required
def budget_create(request):
    if request.method == 'POST':
        form = BudgetForm(request.POST)
        if form.is_valid():
            budget = form.save(commit=False)
            budget.user = request.user
            budget.save()
            messages.success(request, "Budget created successfully.")
            return redirect('budgets:budget_list')
    else:
        form = BudgetForm()
    return render(request, 'budgets/budget_form.html', {'form': form})


@login_required
def budget_update(request, pk):
    budget = get_object_or_404(Budget, pk=pk, user=request.user)
    if request.method == 'POST':
        form = BudgetForm(request.POST, instance=budget)
        if form.is_valid():
            form.save()
            messages.success(request, "Budget updated successfully.")
            return redirect('budgets:budget_list')
    else:
        form = BudgetForm(instance=budget)
    return render(request, 'budgets/budget_form.html', {'form': form})


@login_required
def budget_delete(request, pk):
    budget = get_object_or_404(Budget, pk=pk, user=request.user)
    if request.method == 'POST':
        budget.delete()
        messages.success(request, "Budget deleted successfully.")
        return redirect('budgets:budget_list')
    return render(request, 'budgets/budget_confirm_delete.html', {'budget': budget})
