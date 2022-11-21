from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView,DetailView,DeleteView,UpdateView
from order.models import OrderItem

# Create your views here.

class Dashboard(LoginRequiredMixin,ListView):
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