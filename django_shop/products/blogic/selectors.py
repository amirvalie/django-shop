from django.db.models import Q
from django.shortcuts import get_object_or_404

from ..models import (
    Product,
    IpAddress,
    Brand,
)
from ...categories.models import Banner
from ...categories.blogic.selectors import get_category, get_banner
from typing import Iterable, Any
from rest_framework.response import Response
from django_filters import rest_framework as filters


class ProudctFilter(filters.FilterSet):
    class Meta:
        model = Product
        fields = ['title']


def product_list(filters=None) -> Iterable[Product]:
    if filters:
        filters = filters or {}
        products = Product.objects.product_publish()
        return ProudctFilter(filters, products).qs
    return Product.objects.product_publish()


def most_visited_products() -> Iterable[Product]:
    return Product.objects.number_of_visits().order_by('-count')


def session_discount() -> Iterable[Banner]:
    return Banner.objects.filter(
        status='p',
        type_category='seasonal'
    )


def special_offer_category() -> Iterable[Banner]:
    return Banner.objects.filter(
        status='p',
        type_category='special_offer'
    )[:10]


def brand_list() -> Iterable[Brand]:
    return Brand.objects.all()


def get_product(**kwargs) -> Product:
    return get_object_or_404(Product, **kwargs)


def related_product_list(product: Product) -> Iterable[Product]:
    return Product.objects.filter(
        title__icontains=product.title[:5]
    ).exclude(id=product.id)


def product_search(query: str) -> Iterable[Product]:
    return Product.objects.filter(Q(title__icontain=query) |
                                  Q(slug__icontain=query)
                                  )


def category_products(slug: str) -> Iterable[Product]:
    category = get_category(slug)
    return category.category_products.product_publish()


def special_offers(slug: str) -> Iterable[Product]:
    banner = get_banner(slug)
    return banner.banner_products.product_publish()


def discounted_products() -> Iterable[Product]:
    return Product.objects.discounted_products()


def best_selling_products() -> Iterable[Product]:
    return Product.objects.product_sales().order_by('-max_sales_number')


def get_brand(brand_name: str) -> Brand:
    return get_object_or_404(Brand, brand_name=brand_name)


def brand_products(brand_name: str) -> Iterable[Product]:
    brand = get_brand(brand_name)
    return brand.products.product_publish()


def get_response_paginator(paginator_class, queryset, serializer_class, request, view) -> Response | Any:
    paginator = paginator_class()
    page = paginator.paginate_queryset(queryset, request, view=view)
    if page is not None:
        serializer = serializer_class(page, many=True)
        return paginator.get_paginated_response(serializer.data)

    serializer = serializer_class(queryset, many=True)
    return Response(data=serializer.data)
