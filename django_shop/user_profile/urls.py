from django.urls import path
from .views import (
        OrderListView,
        CreateOrListAddressView,
        DeleteAddressView,
        UpdateAddressView,
        UserInfoView,
        DashboardView,
        PasswordChangeView,
    )

app_name = 'profile'
urlpatterns = [
    path('orders/',OrderListView.as_view(),name='orders'),
    path('address/',CreateOrListAddressView.as_view(),name='address'),
    path('address/delete/<int:pk>/',DeleteAddressView.as_view(),name='delete_address'),
    path('address/update/<int:pk>/',UpdateAddressView.as_view(),name='update_address'),
    path('user/',UserInfoView.as_view(),name='user_info'),
    path('dashboard/',DashboardView.as_view(),name='dashboard'),
    path('change_password/',PasswordChangeView.as_view(),name='change_password'),
]