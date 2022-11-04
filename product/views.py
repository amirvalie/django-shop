from django.shortcuts import get_object_or_404, render,HttpResponse
from product.models import (
        Product,
        MainCategory,
        Banner,
        Brand,
        IpAddress,
    )
from django.views.generic import (ListView,DetailView)
from django.db.models import Q
from cart.forms import CartAddProductFrom
# Create your views here.



class ListProduct(ListView):
    queryset=Product.objects.product_publish()[:16]
    template_name='product/home.html'
    context_object_name='products'

    def get_context_data(self,**kwargs):
        context=super().get_context_data(**kwargs)
        context['most_visit_product']=Product.objects.number_of_visits().order_by('-count')[:16]
        context['categories']=MainCategory.objects.filter(
            status='p',
            parent__isnull=True
        )
        context['season_discounts']=Banner.objects.filter(
            status='p',
            type_category='seasonal'
        )[:2]
        context['special_offers']=Banner.objects.filter(
            status='p',
            type_category='special_offer'
        )[:10]
        context['brands']=Brand.objects.all()
        return context

