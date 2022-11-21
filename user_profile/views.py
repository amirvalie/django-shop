from django.shortcuts import render
from django.views.generic import ListView,DetailView,DeleteView,UpdateView
from order.models import OrderItem
from .models import Address
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View
from .forms import AddressForm,UserForm
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.urls import reverse_lazy
from django.shortcuts import get_object_or_404
from django.contrib.auth.views import PasswordChangeView
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import PasswordChangeForm,SetPasswordForm
User=get_user_model()

class DashboardView(LoginRequiredMixin,ListView):
    template_name='profile/dashboard.html'
    def get_queryset(self):
        orderitems=OrderItem.objects.filter(
            order__user=self.request.user,
        )
        return orderitems

    def get_context_data(self,**kwargs):
        context=super().get_context_data(**kwargs)
        context['sending']=self.get_queryset().filter(order__status='sending').count()
        context['delivered']=self.get_queryset().filter(order__status='delivered').count()
        context['returned']=self.get_queryset().filter(order__status='returned').count()
        return context


class OrderListView(LoginRequiredMixin,ListView):
    template_name='profile/orders.html'
    context_object_name='orderitems'
    model=OrderItem
    def get_queryset(self):
        if self.request.GET.get('q') in ['sending','delivered','returned']:
            orderitems=OrderItem.objects.filter(
                order__user=self.request.user,
                order__status=self.request.GET.get('q'),
            )
        else:
            orderitems=OrderItem.objects.filter(
                order__user=self.request.user,
            )
        if self.request.GET.get('issue_tracking',None):
            orderitems=orderitems.filter(
                issue_tracking=self.request.GET.get('issue_tracking',None),
            )
        return orderitems