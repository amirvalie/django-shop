from django import template
from ...categories.models import Category
from ..models import Product
from django.http import request
from persiantools.jdatetime import JalaliDate

register = template.Library()


@register.inclusion_tag("product/navbar/navbar.html", takes_context=True)
def navbar(context):
    request = context['request']
    return {
        'categories': Category.objects.category_publish(),
        'request': request
    }


@register.filter
def price_format(variable):
    variable = int(variable)
    return '{:,}'.format(variable)


@register.filter
def product_rates(obj_id):
    return Product.objects.avg_rates(obj_id)


@register.filter
def count_rates(obj_id):
    return Product.objects.count_rates(obj_id)


@register.filter()
def jalali_day_name(date):
    jalali_date = JalaliDate(date)
    day_name = jalali_date.strftime('%A', 'fa')
    return day_name


@register.filter()
def jalali_date(date):
    jalali_date = JalaliDate(date)
    return jalali_date
