from django.shortcuts import redirect, render, HttpResponse
from ..cart.cart import Cart
from .models import OrderItem, Order, DatePikcer
from django.contrib.auth import get_user_model
from django.views import View
from ..user_profile.models import Address
from django.views.generic import ListView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from .mixins import ProductExistMixin
from ..coupon.forms import CouponApplyForm
from django.utils import timezone
import datetime
from django.core.exceptions import BadRequest
from .forms import OrderCreateForm, ChoicesForm
from .blogic.selectors import (
    dates_list,
    date_get,
)
from ..user_profile.blogic.selectors import (
    address_list,
    active_address,
    get_address
)
from .blogic.services import activate_address, order_create
User = get_user_model()


class SelectAddressView(LoginRequiredMixin, ProductExistMixin, View):
    template_name = 'order/address_list.html'

    def get_queryset(self):
        return address_list(user=self.request.user)

    def get(self, request, *args, **kwargs):
        context = dict()
        context["cart"] = Cart(self.request)
        context['addresses'] = self.get_queryset()
        if self.get_queryset():
            context['active_address'] = self.get_queryset().get(
                active_address=True,
            )
        else:
            context['active_address'] = None
        context['form'] = CouponApplyForm()
        context['datepicker'] = dates_list()
        return render(request, self.template_name, context)


class ActiveAddressView(View):
    def post(self, request, *args, **kwargs):
        old_active_address = active_address(user=request.user)
        choices = [
            (f'{obj_id}', f'address_{obj_id}')
            for obj_id in address_list(user=self.request.user).values_list('id', flat=True)
        ]
        form = ChoicesForm(data=request.POST, obj_ids=choices)
        if form.is_valid():
            pk = form.cleaned_data['choice_field']
            new_active_address = get_address(pk=pk)
            activate_address(
                new_active_address=new_active_address,
                old_active_address=old_active_address,
            )

        return redirect('orders:checkout')


class CreateOrder(LoginRequiredMixin, View):

    def post(self, request, *args, **kwargs):
        dates = dates_list()
        choices = [
            (f'{obj_id}', f'datepicker_{obj_id}')
            for obj_id in dates.values_list('id', flat=True)
        ]
        form = ChoicesForm(data=request.POST, obj_ids=choices)
        if form.is_valid():
            cart = Cart(request)
            active_address = get_address(user=request.user, active_address=True)
            date = date_get(id=form.cleaned_data['choice_field'])
            order_create(
                request=request,
                active_address=active_address,
                status='unpaid',
                date=date,
                cart=cart
            )
            return redirect('profile:orders')
        else:
            return redirect('orders:checkout')
