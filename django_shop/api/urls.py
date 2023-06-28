from django.urls import path, include

urlpatterns = [
    path('', include(('django_shop.products.urls', 'product'))),
    path('', include(('django_shop.django_phone_login.urls', 'django_phone_login'))),
]