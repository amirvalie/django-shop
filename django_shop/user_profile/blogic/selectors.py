from ..models import Address
from django.shortcuts import get_object_or_404
from typing import Iterable

def active_address() -> Address:
    return Address.objects.get(
        active_addres=True
    )


def get_address(**kwargs) -> Address:
    return get_object_or_404(Address, **kwargs)


def address_list(*, user) -> Iterable[Address]:
    return Address.objects.filter(
        user=user
    )
