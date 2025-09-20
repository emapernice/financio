from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import Currency, Entity, CurrencyExchange
from .forms import CurrencyForm, EntityForm, CurrencyExchangeForm


def home(request):
    return render(request, 'home.html')


@login_required
def currency_list(request):
    currencies = Currency.objects.all()
    return render(request, 'core/currency_list.html', {'currencies': currencies})


@login_required
def currency_create(request):
    if request.method == 'POST':
        form = CurrencyForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Currency created successfully.")
            return redirect('core:currency_list')
    else:
        form = CurrencyForm()
    return render(request, 'core/currency_form.html', {'form': form})


@login_required
def currency_update(request, pk):
    currency = get_object_or_404(Currency, pk=pk)
    if request.method == 'POST':
        form = CurrencyForm(request.POST, instance=currency)
        if form.is_valid():
            form.save()
            messages.success(request, "Currency updated successfully.")
            return redirect('core:currency_list')
    else:
        form = CurrencyForm(instance=currency)
    return render(request, 'core/currency_form.html', {'form': form})


@login_required
def currency_delete(request, pk):
    currency = get_object_or_404(Currency, pk=pk)
    if request.method == 'POST':
        currency.delete()
        messages.success(request, "Currency deleted successfully.")
        return redirect('core:currency_list')
    return render(request, 'core/currency_confirm_delete.html', {'currency': currency})


@login_required
def entity_list(request):
    entities = Entity.objects.all()
    return render(request, 'core/entity_list.html', {'entities': entities})


@login_required
def entity_create(request):
    if request.method == 'POST':
        form = EntityForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Entity created successfully.")
            return redirect('core:entity_list')
    else:
        form = EntityForm()
    return render(request, 'core/entity_form.html', {'form': form})


@login_required
def entity_update(request, pk):
    entity = get_object_or_404(Entity, pk=pk)
    if request.method == 'POST':
        form = EntityForm(request.POST, instance=entity)
        if form.is_valid():
            form.save()
            messages.success(request, "Entity updated successfully.")
            return redirect('core:entity_list')
    else:
        form = EntityForm(instance=entity)
    return render(request, 'core/entity_form.html', {'form': form})


@login_required
def entity_delete(request, pk):
    entity = get_object_or_404(Entity, pk=pk)
    if request.method == 'POST':
        entity.delete()
        messages.success(request, "Entity deleted successfully.")
        return redirect('core:entity_list')
    return render(request, 'core/entity_confirm_delete.html', {'entity': entity})


@login_required
def exchange_list(request):
    exchanges = CurrencyExchange.objects.all()
    return render(request, 'core/exchange_list.html', {'exchanges': exchanges})


@login_required
def exchange_create(request):
    if request.method == 'POST':
        form = CurrencyExchangeForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Exchange created successfully.")
            return redirect('core:exchange_list')
    else:
        form = CurrencyExchangeForm()
    return render(request, 'core/exchange_form.html', {'form': form})


@login_required
def exchange_update(request, pk):
    exchange = get_object_or_404(CurrencyExchange, pk=pk)
    if request.method == 'POST':
        form = CurrencyExchangeForm(request.POST, instance=exchange)
        if form.is_valid():
            form.save()
            messages.success(request, "Exchange updated successfully.")
            return redirect('core:exchange_list')
    else:
        form = CurrencyExchangeForm(instance=exchange)
    return render(request, 'core/exchange_form.html', {'form': form})


@login_required
def exchange_delete(request, pk):
    exchange = get_object_or_404(CurrencyExchange, pk=pk)
    if request.method == 'POST':
        exchange.delete()
        messages.success(request, "Exchange deleted successfully.")
        return redirect('core:exchange_list')
    return render(request, 'core/exchange_confirm_delete.html', {'exchange': exchange})
