from datetime import date, timedelta
from dateutil.relativedelta import relativedelta
from records.models import Record
from .models import FixedRecord  

def process_fixed_records():
    today = date.today()
    fixed_records = FixedRecord.objects.filter(next_execution__lte=today, is_active=True)

    for fixed in fixed_records:
        Record.objects.create(
            record_type=fixed.record_type,
            account=fixed.account,
            record_amount=fixed.amount,
            currency=fixed.account.currency,
            subcategory=fixed.subcategory,
            record_description=f"Fixed record ({fixed.frequency})",
            record_date=fixed.next_execution,
        )

        if fixed.frequency == "daily":
            fixed.next_execution += timedelta(days=1)
        elif fixed.frequency == "weekly":
            fixed.next_execution += timedelta(weeks=1)
        elif fixed.frequency == "monthly":
            fixed.next_execution += relativedelta(months=1)
        elif fixed.frequency == "yearly":
            fixed.next_execution += relativedelta(years=1)

        if fixed.end_date and fixed.next_execution > fixed.end_date:
            fixed.is_active = False

        fixed.save(update_fields=["next_execution", "is_active"])
