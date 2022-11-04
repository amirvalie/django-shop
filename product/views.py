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

class ProductDetail(DetailView):
    template_name='product/detail.html' 
    context_object_name='product'

    def get_object(self):
        slug=self.kwargs.get('slug')
        product=get_object_or_404(Product.objects.product_publish(),slug=slug)
        ip_address=self.request.user.ip_address
        if not ip_address in product.visits.values_list('ip',flat=True):
            ip_object=IpAddress.objects.create(
                ip=ip_address
            )
            product.visits.add(
                ip_object
            )
        return product  

    def get_context_data(self,**kwargs):
        context=super().get_context_data(**kwargs)
        product=context.get('product')
        related_product=Product.objects.filter(title__icontains=product.title[:5]).exclude(id=product.id)[:5]
        context['related_products']=related_product
        context['form']=CartAddProductFrom()
        return context   