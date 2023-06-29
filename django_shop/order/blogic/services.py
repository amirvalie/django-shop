from django.db import transaction
from ..models import Address, OrderItem, Order, DatePikcer
from django.http import HttpRequest


@transaction.atomic
def activate_address(*,
                     old_active_address: Address,
                     new_active_address: Address) -> None:
    old_active_address.active_address = False
    new_active_address.active_address = True
    old_active_address.save()
    new_active_address.save()


def order_create(*, request: HttpRequest,
                 active_address: Address,
                 status: str,
                 date: DatePikcer,
                 cart: None):
    order_obj = Order.objects.create(
        user=request.user,
        address=active_address,
        status=status,
        datepikcer=date,
    )

    for item in cart:
        OrderItem.objects.create(
            order=order_obj,
            product=item['product'],
            price=item['price'],
            color=item['color'] if item['color'] is not None else None,
            size=item['size'] if item['size'] is not None else None,
        )
    cart.clear()
