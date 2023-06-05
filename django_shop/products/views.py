from django.shortcuts import get_object_or_404, render, HttpResponse
from django.views.generic import (ListView, DetailView)
from django.db.models import Q
from cart.forms import CartAddProductFrom
from .models import (
    Product,
    Brand,
    IpAddress,
)

from .blogic.selectors import (
    product_list,
    most_visited_products,
    session_discount,
    special_offer_category,
    brand_list,
    get_product,
    related_product_list,
    product_search,
    category_products,
    special_offers,
    discounted_products,
    best_selling_products,
)
from .blogic.services import (
    add_user_to_product_visits
    )
from ..categories.blogic.selectors import category_list


# Create your views here.


class Home(ListView):
    queryset = product_list()[:16]
    template_name = 'product/home.html'
    context_object_name = 'products'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['most_visit_product'] = most_visited_products()[:16]
        context['categories'] = category_list()
        context['season_discounts'] = session_discount()[:2]
        context['special_offers'] = special_offer_category()[:10]
        context['brands'] = brand_list()[10]
        return context


class ProductDetail(DetailView):
    template_name = 'product/detail.html'
    context_object_name = 'product'

    def get_object(self):
        slug = self.kwargs.get('slug')
        product = get_product(slug)
        ip_address = self.request.user.ip_address
        add_user_to_product_visits(product, ip_address)
        return product

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        product = context.get('product')
        context['related_products'] = related_product_list(product=context['product'])
        context['form'] = CartAddProductFrom()
        return context


class ProductSearch(ListView):
    template_name = 'product/search_result.html'
    context_object_name = 'products'
    model = Product
    paginate_by = 10

    def get_queryset(self):
        query = self.request.GET.get('q', "None")
        object_list = product_search(query=query)
        return object_list


class ProductsInCategory(ListView):
    template_name = 'product/list.html'
    context_object_name = 'products'
    paginate_by = 10

    def get_queryset(self):
        slug = self.kwargs.get('slug')
        return category_products(slug)


class SpecialOffer(ListView):
    template_name = 'product/list.html'
    context_object_name = 'products'
    paginate_by = 10

    def get_queryset(self):
        slug = self.kwargs.get('slug')
        return special_offers(slug)

class DiscountedProduct(ListView):
    template_name = 'product/discounted_products.html'
    context_object_name = 'products'
    paginate_by = 4
    queryset = discounted_products()


class BestSellingProduct(ListView):
    template_name = 'product/best_selling_products.html'
    context_object_name = 'products'
    paginate_by = 4
    queryset = best_selling_products()[:20]


class BrandProduct(ListView):
    template_name = 'product/brand_landing.html'
    context_object_name = 'products'
    paginate_by = 4

    def get_queryset(self):
        brand_name = self.kwargs.get('brand_name')
        brand = get_object_or_404(Brand, brand_name=brand_name)
        return brand.products.product_publish()
