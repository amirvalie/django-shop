from typing import Iterable
from django.shortcuts import get_object_or_404
from ..models import (
        Category,
        Banner
    )


def category_list() -> Iterable[Category]:
    return Category.objects.filter(
        status='p',
        parent__isnull=True
    )

def get_category(slug:str) -> Category:
    return get_object_or_404(
        Category,
        slug=slug
    )

def get_banner(slug:str) -> Banner:
    return get_object_or_404(
        Banner(),
        slug=slug
    )   