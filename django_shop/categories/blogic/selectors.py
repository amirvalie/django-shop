from typing import Iterable

from ..models import Category


def category_list() -> Iterable[Category]:
    return Category.objects.filter(
        status='p',
        parent__isnull=True
    )
