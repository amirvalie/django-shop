from django.shortcuts import redirect, render,HttpResponse
from cart.cart import Cart
from .models import OrderItem,Order,DatePikcer
from django.contrib.auth import get_user_model
from django.views import View
from user_profile.models import Address
from django.views.generic import ListView,DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from .mixins import ProductExistMixin
User=get_user_model()
from coupon.forms import CouponApplyForm
from django.utils import timezone
import datetime
from django.core.exceptions import BadRequest

class SelectAddressView(LoginRequiredMixin,ProductExistMixin,View):
    template_name='order/address_list.html'

    def get_queryset(self):
        queryset = Address.objects.filter(
            user=self.request.user
        ).order_by('-id')
        return queryset

    def get(self,request,*args,**kwargs):
        context={}
        context["cart"] =Cart(self.request)
        context['addresses']=self.get_queryset()
        if self.get_queryset():
            context['active_address']=self.get_queryset().get(
                active_address=True,
            )
        else:
            context['active_address']=None
        context['form']=CouponApplyForm()
        context['datepicker']=DatePikcer.objects.filter(
            date__gte=timezone.now().date(),
            date__lte=timezone.now().date() + datetime.timedelta(days=5),
            active=True,
        )
        return render(request,self.template_name,context)