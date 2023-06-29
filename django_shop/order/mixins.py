from ..cart.cart import Cart
from django.shortcuts import redirect

class ProductExistMixin(object):
    def dispatch(self, request, *args, **kwargs):
        cart=Cart(request)
        if cart.__len__() >= 1:
            return super(ProductExistMixin, self).dispatch(request, *args, **kwargs)
        else:
            return redirect('cart:cart_detail')


