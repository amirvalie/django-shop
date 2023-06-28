from django.shortcuts import render
from django.utils import timezone
from .forms import CouponApplyForm
from .models import Coupon
from django.shortcuts import redirect
from django.views.decorators.http import require_POST
from django.views.generic.edit import FormView
from django.http import HttpResponse
from .selectors import get_coupon
# Create your views here.


@require_POST
def coupon_apply(request):
    now = timezone.now()
    if request.method == 'POST':
        form = CouponApplyForm(request.POST)
        if form.is_valid():
            code = form.cleaned_data['code']
            try:
                coupon = get_coupon(code=code)
                request.session['coupon_id'] = coupon.id
            except Coupon.DoesNotExist:
                request.session['coupon_id'] = None
        return redirect('orders:checkout')
    else:
        return HttpResponse("Invalid request")