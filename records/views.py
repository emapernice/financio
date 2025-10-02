from django.core.paginator import Paginator
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import Record, Category, Subcategory, Account
from .forms import RecordForm, CategoryForm, SubcategoryForm


# -------------------- Record --------------------

@login_required
def record_list(request):
    records = Record.objects.select_related('account', 'currency', 'subcategory__category') \
                            .filter(account__user=request.user) \
                            .order_by('-record_date')

    accounts = Account.objects.filter(user=request.user)

    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')
    account = request.GET.get('account')
    record_type = request.GET.get('record_type')

    if start_date:
        records = records.filter(record_date__gte=start_date)
    if end_date:
        records = records.filter(record_date__lte=end_date)
    if account:
        records = records.filter(account_id=account, account__user=request.user)  
    if record_type:
        records = records.filter(record_type=record_type)

    paginator = Paginator(records, 25)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'accounts': accounts,
        'page_obj': page_obj,
        'start_date': start_date,
        'end_date': end_date,
        'selected_account': account,
        'selected_record_type': record_type,
    }
    return render(request, 'records/record_list.html', context)


@login_required
def record_create(request):
    if request.method == 'POST':
        form = RecordForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Record saved successfully.")
            return redirect('records:record_list')
    else:
        form = RecordForm()
    return render(request, 'records/record_form.html', {'form': form})


@login_required
def record_update(request, pk):
    record = get_object_or_404(Record, pk=pk)
    if request.method == 'POST':
        form = RecordForm(request.POST, instance=record)
        if form.is_valid():
            form.save()
            messages.success(request, "Record updated successfully.")
            return redirect('records:record_list')
    else:
        form = RecordForm(instance=record)
    return render(request, 'records/record_form.html', {'form': form})


@login_required
def record_delete(request, pk):
    record = get_object_or_404(Record, pk=pk)
    if request.method == 'POST':
        record.delete()
        messages.success(request, "Record deleted successfully.")
        return redirect('records:record_list')
    return render(request, 'records/record_confirm_delete.html', {'record': record})


# -------------------- Category --------------------

@login_required
def category_list(request):
    categories = Category.objects.all().order_by('category_name')
    paginator = Paginator(categories, 25)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'records/category_list.html', {'page_obj': page_obj})


@login_required
def category_create(request):
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Category saved successfully.")
            return redirect('records:category_list')
    else:
        form = CategoryForm()
    return render(request, 'records/category_form.html', {'form': form})


@login_required
def category_update(request, pk):
    category = get_object_or_404(Category, pk=pk)
    if request.method == 'POST':
        form = CategoryForm(request.POST, instance=category)
        if form.is_valid():
            form.save()
            messages.success(request, "Category updated successfully.")
            return redirect('records:category_list')
    else:
        form = CategoryForm(instance=category)
    return render(request, 'records/category_form.html', {'form': form})


@login_required
def category_delete(request, pk):
    category = get_object_or_404(Category, pk=pk)
    if request.method == 'POST':
        category.delete()
        messages.success(request, "Category deleted successfully.")
        return redirect('records:category_list')
    return render(request, 'records/category_confirm_delete.html', {'category': category})


# -------------------- Subcategory --------------------

@login_required
def subcategory_list(request):
    subcategories = Subcategory.objects.select_related('category').order_by('subcategory_name')
    paginator = Paginator(subcategories, 25)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'records/subcategory_list.html', {'page_obj': page_obj})


@login_required
def subcategory_create(request):
    if request.method == 'POST':
        form = SubcategoryForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Subcategory saved successfully.")
            return redirect('records:subcategory_list')
    else:
        form = SubcategoryForm()
    return render(request, 'records/subcategory_form.html', {'form': form})


@login_required
def subcategory_update(request, pk):
    subcategory = get_object_or_404(Subcategory, pk=pk)
    if request.method == 'POST':
        form = SubcategoryForm(request.POST, instance=subcategory)
        if form.is_valid():
            form.save()
            messages.success(request, "Subcategory updated successfully.")
            return redirect('records:subcategory_list')
    else:
        form = SubcategoryForm(instance=subcategory)
    return render(request, 'records/subcategory_form.html', {'form': form})


@login_required
def subcategory_delete(request, pk):
    subcategory = get_object_or_404(Subcategory, pk=pk)
    if request.method == 'POST':
        subcategory.delete()
        messages.success(request, "Subcategory deleted successfully.")
        return redirect('records:subcategory_list')
    return render(request, 'records/subcategory_confirm_delete.html', {'subcategory': subcategory})
