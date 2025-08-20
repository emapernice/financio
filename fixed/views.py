from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import FixedRecord
from .forms import FixedRecordForm


@login_required
def fixedrecord_list(request):
    fixedrecords = FixedRecord.objects.all()
    return render(request, 'fixed/fixedrecord_list.html', {'fixedrecords': fixedrecords})


@login_required
def fixedrecord_create(request):
    if request.method == 'POST':
        form = FixedRecordForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Fixed record created successfully.")
            return redirect('fixed:fixedrecord_list')
    else:
        form = FixedRecordForm()
    return render(request, 'fixed/fixedrecord_form.html', {'form': form})


@login_required
def fixedrecord_update(request, pk):
    fixedrecord = get_object_or_404(FixedRecord, pk=pk)
    if request.method == 'POST':
        form = FixedRecordForm(request.POST, instance=fixedrecord)
        if form.is_valid():
            form.save()
            messages.success(request, "Fixed record updated successfully.")
            return redirect('fixed:fixedrecord_list')
    else:
        form = FixedRecordForm(instance=fixedrecord)
    return render(request, 'fixed/fixedrecord_form.html', {'form': form})


@login_required
def fixedrecord_delete(request, pk):
    fixedrecord = get_object_or_404(FixedRecord, pk=pk)
    if request.method == 'POST':
        fixedrecord.delete()
        messages.success(request, "Fixed record deleted successfully.")
        return redirect('fixed:fixedrecord_list')
    return render(request, 'fixed/fixedrecord_confirm_delete.html', {'fixedrecord': fixedrecord})
