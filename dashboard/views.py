from decimal import Decimal
from django.db.models import Sum
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from accounts.models import Account
from records.models import Record
from investments.models import Investment


@login_required
def dashboard_view(request):
    user = request.user  

    accounts = Account.objects.filter(user=user)
    investments = Investment.objects.filter(account__user=user, status="active")  

    accounts_data = []
    for acc in accounts:
        income = acc.records.filter(record_type="income").aggregate(total=Sum("record_amount"))["total"] or Decimal("0")
        expense = acc.records.filter(record_type="expense").aggregate(total=Sum("record_amount"))["total"] or Decimal("0")
        available = acc.initial_balance + income - expense

        invs = investments.filter(account=acc)
        inv_capital = sum((inv.amount for inv in invs), Decimal("0"))
        inv_interest = sum((Decimal(inv.expected_interest) for inv in invs), Decimal("0"))
        inv_total = inv_capital + inv_interest

        total_balance = available + inv_total

        accounts_data.append({
            "account": acc,
            "income": income,
            "expense": expense,
            "available": available,
            "inv_capital": inv_capital,
            "inv_interest": inv_interest,
            "inv_total": inv_total,
            "total_balance": total_balance,
        })

    balances_by_currency = {}
    for acc in accounts_data:
        code = acc["account"].currency.currency_code
        balances_by_currency.setdefault(code, {
            "available": Decimal("0"),
            "inv_capital": Decimal("0"),
            "inv_interest": Decimal("0"),
            "inv_total": Decimal("0"),
        })
        balances_by_currency[code]["available"] += acc["available"]
        balances_by_currency[code]["inv_capital"] += acc["inv_capital"]
        balances_by_currency[code]["inv_interest"] += acc["inv_interest"]
        balances_by_currency[code]["inv_total"] += acc["inv_total"]

    context = {
        "accounts_data": accounts_data,
        "balances_by_currency": balances_by_currency,
    }
    return render(request, "dashboard/dashboard.html", context)
