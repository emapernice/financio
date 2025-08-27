from django.utils import timezone
from .models import Investment
from .services import create_investment_inflow


def close_expired_investments():
    today = timezone.now().date()
    investments = Investment.objects.filter(status="active", end_date=today)

    for inv in investments:
        create_investment_inflow(inv, inv.account.user)
        inv.status = "closed"
        inv.save(update_fields=["status"])            
