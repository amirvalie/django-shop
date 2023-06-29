from django.shortcuts import render
from django.views.generic import ListView, DetailView, DeleteView, UpdateView
from ..order.models import OrderItem
from .models import Address
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View
from .forms import AddressForm, UserForm
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.urls import reverse_lazy
from django.shortcuts import get_object_or_404
from django.contrib.auth.views import PasswordChangeView
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import PasswordChangeForm, SetPasswordForm
from ..order.blogic.selectors import list_order_item
User = get_user_model()


class DashboardView(LoginRequiredMixin, ListView):
    template_name = 'profile/dashboard.html'

    def get_queryset(self):
        return list_order_item(user=self.request.user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['sending'] = self.get_queryset().filter(order__status='sending').count()
        context['delivered'] = self.get_queryset().filter(order__status='delivered').count()
        context['returned'] = self.get_queryset().filter(order__status='returned').count()
        return context


class OrderListView(LoginRequiredMixin, ListView):
    template_name = 'profile/orders.html'
    context_object_name = 'orderitems'
    model = OrderItem

    def get_queryset(self):
        if self.request.GET.get('q') in ['sending', 'delivered', 'returned']:
            orderitems = OrderItem.objects.filter(
                order__user=self.request.user,
                order__status=self.request.GET.get('q'),
            )
        else:
            orderitems = OrderItem.objects.filter(
                order__user=self.request.user,
            )
        if self.request.GET.get('issue_tracking', None):
            orderitems = orderitems.filter(
                issue_tracking=self.request.GET.get('issue_tracking', None),
            )
        return orderitems


class CreateOrListAddressView(LoginRequiredMixin, View):
    template_name = 'profile/address.html'
    form_class = AddressForm

    def get_queryset(self):
        addresses = Address.objects.filter(
            user=self.request.user,
        ).order_by('-id')
        return addresses

    def get(self, request, *args, **kwargs):
        form = self.form_class()
        return render(request, self.template_name, {'addresses': self.get_queryset(), 'form': form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            if self.get_queryset().count() >= 1:
                curent_active_address = self.get_queryset().get(active_address=True)
                curent_active_address.active_address = False
                curent_active_address.save()
            address = form.save(commit=False)
            address.user = request.user
            address.active_address = True
            address.save()
            return HttpResponseRedirect(reverse('profile:address'))
        return render(request, self.template_name, {'addresses': self.get_queryset(), 'form': form})


class DeleteAddressView(LoginRequiredMixin, DeleteView):
    model = Address
    template_name = 'profile/delete_confirm.html'
    success_url = reverse_lazy('profile:address')

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        success_url = self.get_success_url()
        self.object.delete()
        last_object = Address.objects.filter(
            user=request.user,
        ).last()
        if last_object:
            last_object.active_address = True
            last_object.save()
        return HttpResponseRedirect(success_url)


class UpdateAddressView(LoginRequiredMixin, UpdateView):
    model = Address
    form_class = AddressForm
    template_name = 'profile/update_address.html'
    success_url = reverse_lazy('profile:address')


class UserInfoView(LoginRequiredMixin, UpdateView):
    form_class = UserForm
    template_name = 'profile/user_info.html'
    success_url = reverse_lazy('profile:user_info')

    def get_object(self):
        return get_object_or_404(User, pk=self.request.user.pk)


class PasswordChangeView(PasswordChangeView):
    template_name = 'profile/password_change.html'
    form_class = [PasswordChangeForm, SetPasswordForm]
    success_url = reverse_lazy('profile:user_info')

    def get_form_class(self):
        """Return the form class to use."""
        if self.request.user.password:
            return self.form_class[0]
        return self.form_class[1]
