from django.urls import path
from .views import coupon_apply

app_name='coupon'
urlpatterns=[
    path('apply/',coupon_apply,name="coupon_apply")
]