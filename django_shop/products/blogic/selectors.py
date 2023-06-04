from ..models import (
    Product,
    IpAddress,
    Brand,
    Banner,
)
from typing import Iterable


def product_list() -> Iterable[Product]:
    return Product.objects.product_publish()


def most_visited_products() -> Iterable[Product]:
    return Product.objects.number_of_visits().order_by('-count')


def session_discount() -> Iterable[Banner]:
    return Banner.objects.filter(
        status='p',
        type_category='seasonal'
    )


def special_offer() -> Iterable[Banner]:
    return Banner.objects.filter(
        status='p',
        type_category='special_offer'
    )[:10]


def brand_list() -> Iterable[Brand]:
    return Brand.objects.all()
