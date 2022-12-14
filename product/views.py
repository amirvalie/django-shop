from django.shortcuts import get_object_or_404, render,HttpResponse
from django.views.generic import (ListView,DetailView)
from django.db.models import Q
from cart.forms import CartAddProductFrom
from product.models import (
        Product,
        MainCategory,
        Banner,
        Brand,
        IpAddress,
    )
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

class ProductSearch(ListView):
    template_name='product/search_result.html'
    context_object_name='products'
    model=Product
    paginate_by=10
    def get_queryset(self):
        query=self.request.GET.get('q',"None")
        object_list=Product.objects.filter(Q(title__icontains=query) | Q(slug__icontains=query))
        return object_list

class ProductsInCategory(ListView):
    template_name='product/list.html'
    context_object_name='products'
    paginate_by=10
    def get_queryset(self):
        slug=self.kwargs.get('slug')
        category=get_object_or_404(MainCategory.objects.category_publish(),slug=slug)
        return category.products.product_publish()

class SpecialOffer(ListView):
    template_name='product/list.html'
    context_object_name='products'
    paginate_by=10
    def get_queryset(self):
        slug=self.kwargs.get('slug')
        category=get_object_or_404(Banner.objects.category_publish(),slug=slug)
        return category.products.product_publish()

class DiscountedProduct(ListView):
    template_name='product/discounted_products.html'
    context_object_name='products'
    paginate_by=4
    queryset=Product.objects.discounted_products()



class BestSellingProduct(ListView):
    template_name='product/best_selling_products.html'
    context_object_name='products'
    paginate_by=4
    queryset=Product.objects.product_sales().order_by('-max_sales_number')[:16]


class BrandProduct(ListView):
    template_name='product/brand_landing.html'
    context_object_name='products'
    paginate_by=4
    def get_queryset(self):
        brand_name=self.kwargs.get('brand_name')
        brand=get_object_or_404(Brand,brand_name=brand_name)
        return brand.products.product_publish()
