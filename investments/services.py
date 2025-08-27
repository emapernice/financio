from django.utils import timezone
from records.models import Record, Subcategory


def create_investment_outflow(investment, user):
    subcat = Subcategory.objects.get(subcategory_name="Investments")
    record = Record.objects.create(
        record_type="expense",
        account=investment.account,
        record_amount=investment.amount,
        currency=investment.account.currency,  
        subcategory=subcat,
        record_description=f"Investment started: {investment.description}",
        record_date=investment.start_date or timezone.now().date(),
    )
    investment.outflow_record = record
    investment.save(update_fields=["outflow_record"])
    return record


def create_investment_inflow(investment, user):
    subcat_capital = Subcategory.objects.get(subcategory_name="Return on investment")
    subcat_interest = Subcategory.objects.get(subcategory_name="Investment interests")

    capital_record = Record.objects.create(
        record_type="income",
        account=investment.account,
        record_amount=investment.amount,
        currency=investment.account.currency, 
        subcategory=subcat_capital,
        record_description=f"Return of capital: {investment.description}",
        record_date=investment.end_date or timezone.now().date(),
    )

    interest_record = None
    if investment.expected_interest > 0:
        interest_record = Record.objects.create(
            record_type="income",
            account=investment.account,
            record_amount=investment.expected_interest,
            currency=investment.account.currency,  
            subcategory=subcat_interest,
            record_description=f"Interest generated: {investment.description}",
            record_date=investment.end_date or timezone.now().date(),
        )

    investment.inflow_record = capital_record
    investment.save(update_fields=["inflow_record"])
    return capital_record, interest_record
