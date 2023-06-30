from django.urls import path, include

urlpatterns = [
    path('', include(('django_shop.products.urls', 'product'))),
    path('', include(('django_shop.django_phone_login.urls', 'django_phone_login'))),
    path('', include(('django_shop.coupon.urls', 'coupon'))),
    path('', include(('django_shop.user_profile.urls', 'user_profile'))),
    path('', include(('django_shop.order.urls', 'order'))),
    path('cart/', include(('django_shop.cart.urls', 'cart'))),
]