from django.db.models import Q
from django.shortcuts import get_object_or_404

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


def get_product(slug: str) -> Product:
    return get_object_or_404(Product, slug=slug)


def related_product_list(product: Product) -> Iterable[Product]:
    return Product.objects.filter(
        title__icontains=product.title[:5]
    ).exclude(id=product.id)


def product_search(query: str) -> Iterable[Product]:
    return Product.objects.filter(Q(title__icontain=query) |
                                  Q(slug__icontain=query)
                                  )
