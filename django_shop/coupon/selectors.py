from .models import Coupon
from django.utils import timezone


def get_coupon(*, code: str) -> Coupon:
    now = timezone.now()
    return Coupon.objects.get(
        code__iexact=code,
        valid_from__lte=now,
        valid_to__gte=now,
    )
