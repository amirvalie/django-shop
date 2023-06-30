from ..models import Address
from django.shortcuts import get_object_or_404
from typing import Iterable
from django.contrib.auth import get_user_model

User = get_user_model()


def active_address(user: User) -> Address:
    return Address.objects.get(
        user=user,
        active_address=True
    )


def get_address(**kwargs) -> Address:
    return get_object_or_404(Address, **kwargs)


def address_list(*, user) -> Iterable[Address]:
    return Address.objects.filter(
        user=user
    )
