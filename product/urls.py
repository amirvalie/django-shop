from django.urls import path
from .views import (
    ListProduct,
    ProductDetail,
    ProductSearch,
    ProductsInCategory,
    SpecialOffer,
    DiscountedProduct,
    BestSellingProduct,
    BrandProduct,
    )

app_name='product'

urlpatterns=[
    path('',ListProduct.as_view(),name='home'), 
    path('search_result/',ProductSearch.as_view(),name='search_result'),
    path('item/<slug:slug>/',ProductDetail.as_view(),name='product_detail'),
    path('category/<slug:slug>/',ProductsInCategory.as_view(),name='category_list'),
    path('discounted_products/',DiscountedProduct.as_view(),name='discounted_products'),
    path('best_selling_product/',BestSellingProduct.as_view(),name='best_selling_product'),
    path('brand_landing/<str:brand_name>',BrandProduct.as_view(),name='brand_landing'),
    path('special_offers/<slug:slug>/',SpecialOffer.as_view(),name='special_category_list'),
]