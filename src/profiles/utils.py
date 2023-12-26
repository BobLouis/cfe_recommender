import datetime


from django.contrib.auth import get_user_model
from django.utils import timezone
from django.db.models import Q, F
from django.db.models.expressions import RawSQL
User = get_user_model()



def get_recent_users(days_ago=7, ids_only=True):
    delta = datetime.timedelta(days=days_ago)
    time_delta = timezone.now() - delta
    # qs = User.objects.filter(Q(date_joined__gte=time_delta) | Q(last_login__gte=time_delta))
    qs = User.objects.filter(Q(id__lte=10))
    if ids_only:
        qs = qs.values_list('id', flat=True)
    return qs