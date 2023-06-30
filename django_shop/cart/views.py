from django.shortcuts import render, HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST
from ..products.models import Product
from ..products.blogic.selectors import get_product
from .cart import Cart
from .forms import CartAddProductFrom
from django.db.models import Q

# Create your views here.


def cart_add(request, product_id):
    cart = Cart(request)
    product = get_product(id=product_id)
    if request.method == "POST":
        form = CartAddProductFrom(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            cart.add(product=product,
                     quantity=cd['quantity'],
                     override_quantity=cd['override'],
                     color=cd['color'],
                     size=cd['size'],
                     )
        return redirect('cart:cart_detail')
    else:
        form = CartAddProductFrom()
        return HttpResponse("form is not valid ")


@require_POST
def cart_remove(request, product_id):
    cart = Cart(request)
    product = get_product(id=product_id)
    cart.remove(product)
    return redirect('cart:cart_detail')


def cart_detail(request):
    cart = Cart(request)
    for item in cart:
        if item['color']:
            try:
                print(item)
                color = item['product'].colors.get(color__name=item['color'])
                item['code'] = color.color.code
            except KeyError:
                item['code'] = None
    return render(request, 'cart/cart_detail.html', {'cart': cart})
