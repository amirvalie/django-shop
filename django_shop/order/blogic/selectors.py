import datetime
from typing import Iterable
from django.shortcuts import get_object_or_404
from django.utils import timezone
from ..models import DatePikcer, OrderItem
from django.contrib.auth import get_user_model

User = get_user_model()


def dates_list() -> Iterable[DatePikcer]:
    return DatePikcer.objects.filter(
        date__gte=timezone.now().date(),
        date__lte=timezone.now().date() + datetime.timedelta(days=5),
        active=True,
    )


def date_get(**kwargs) -> DatePikcer:
    return get_object_or_404(DatePikcer, **kwargs)


def list_order_item(*, user: User) -> Iterable[OrderItem]:
    return OrderItem.objects.filter(
        order__user=user
    ).select_related('order')
