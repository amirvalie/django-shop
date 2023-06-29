import datetime
from typing import Iterable
from django.shortcuts import get_object_or_404
from django.utils import timezone
from ..models import Address, DatePikcer


def address_list(*, user) -> Iterable[Address]:
    return Address.objects.filter(
        user=user
    )


def dates_list() -> Iterable[DatePikcer]:
    return DatePikcer.objects.filter(
        date__gte=timezone.now().date(),
        date__lte=timezone.now().date() + datetime.timedelta(days=5),
        active=True,
    )


def date_get(**kwargs) -> DatePikcer:
    return get_object_or_404(DatePikcer, **kwargs)


def active_address() -> Address:
    return Address.objects.get(
        active_addres=True
    )


def get_address(**kwargs) -> Address:
    return get_object_or_404(Address, **kwargs)
