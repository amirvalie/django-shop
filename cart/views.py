from django.shortcuts import render,HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST
from product.models import Product
from .cart import Cart
from .forms import CartAddProductFrom
from django.db.models import Q
from coupon.forms import CouponApplyForm
# Create your views here.


def cart_add(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)  
    if request.method=="POST":
        form = CartAddProductFrom(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            print(cd['color'])
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


