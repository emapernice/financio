from django.utils import timezone
from records.models import Record


def create_fixed_record_execution(fixed_record, user):
    record = Record.objects.create(
        record_type=fixed_record.record_type,
        account=fixed_record.account,
        record_amount=fixed_record.amount,
        currency=fixed_record.account.currency,
        subcategory=fixed_record.subcategory,
        record_description=f"Fixed record execution ({fixed_record.frequency})",
        record_date=timezone.now().date(),
    )
    return record
