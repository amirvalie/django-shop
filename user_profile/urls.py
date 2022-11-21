from django.urls import path
from .views import (
        OrderListView,
        CreateOrListAddressView,
        DeleteAddressView,
        UpdateAddressView,
        UserInfoView,
        Dashboard,
        PasswordChangeView,
    )

app_name = 'profile'
urlpatterns = [
    path('orders/',OrderListView.as_view(),name='orders'),
    path('address/',CreateOrListAddressView.as_view(),name='address'),
    path('address/delete/<int:pk>/',DeleteAddressView.as_view(),name='delete_address'),
    path('address/update/<int:pk>/',UpdateAddressView.as_view(),name='update_address'),
    path('user/',UserInfoView.as_view(),name='user_info'),
    path('dashboard/',Dashboard.as_view(),name='dashboard'),
    path('change_password/',PasswordChangeViewCustome.as_view(),name='change_password'),
]