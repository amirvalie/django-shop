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
from .forms import OrderCreateForm,ChoicesForm

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



class ActiveAddressView(View):
    def get_queryset(self):
        queryset=Address.objects.filter(
            user=self.request.user,
        )
        return queryset
        
    def post(self,request,*args,**kwargs):
        active_address=self.get_queryset().filter(
            active_address=True
        )[0]
        choices=[
            (f'{obj_id}',f'address_{obj_id}') 
            for obj_id in self.get_queryset().values_list('id',flat=True)
        ]
        form=ChoicesForm(data=request.POST,obj_ids=choices)
        if form.is_valid(): 
            instance=form.cleaned_data['choice_field']
            address=Address.objects.get(id=instance)
            address.active_address=True
            active_address.active_address=False
            active_address.save()
            address.save()

        return redirect('orders:checkout')


class CreateOrder(LoginRequiredMixin,View):
    def get_queryset(self):
        queryset=DatePikcer.objects.filter(
            date__gte=timezone.now().date(),
            date__lte=timezone.now().date() + datetime.timedelta(days=5),
            active=True,
        )
        return queryset

    def post(self,request,*args,**kwargs):
        choices=[
            (f'{obj_id}',f'datepicker_{obj_id}') 
            for obj_id in self.get_queryset().values_list('id',flat=True)
        ]
        form=ChoicesForm(data=request.POST,obj_ids=choices)
        if form.is_valid():
            cart=Cart(request)
            active_address=Address.objects.get(user=request.user,active_address=True)
            get_datepicker=self.get_queryset().get(id=form.cleaned_data['choice_field'])
            order_obj = Order.objects.create(
                user=request.user,
                address=active_address,
                status='unpaid',
                datepikcer=get_datepicker,
            )
            for item in cart:
                OrderItem.objects.create(
                    order=order_obj,
                    product=item['product'],
                    price=item['price'],
                    color=item['color'] if item['color'] is not None else None,
                    size=item['size'] if item['size'] is not None else None,
                )            
            cart.clear()
            return redirect('profile:orders')
        else:
            return redirect('orders:checkout')
