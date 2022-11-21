from django.urls import path
from .views import (
    SelectAddressView,
    ActiveAddressView,
    CreateOrder,
    )

app_name='orders'
urlpatterns=[
    path('choose-address/',ActiveAddressView.as_view(),name="choose_address"),
    path('checkout/',SelectAddressView.as_view(),name="checkout"),
    path('create-order/',CreateOrder.as_view(),name="create_order"),
]