from django.urls import path
from .views import (
    Home,
    ProductDetail,
    ProductSearch,
    ProductsRelatedCategory,
    SpecialOffer,
    DiscountedProduct,
    BestSellingProduct,
    BrandProduct,
)
from .api.product_apis import (
    ProductListApi,
    ProductDetailApi,
    CategoryRelatedProductApi,
    BestSellingProductApi,
    BrandProductApi,
    SpecialOfferProductApi,
    DiscountedProductApi,
)

app_name = 'product'

django_urlpatterns = [
    path('', Home.as_view(), name='home'),
    path('search_result/', ProductSearch.as_view(), name='search_result'),
    path('item/<slug:slug>/', ProductDetail.as_view(), name='product_detail'),
    path('category/<slug:slug>/', ProductsRelatedCategory.as_view(), name='category_list'),
    path('discounted_products/', DiscountedProduct.as_view(), name='discounted_products'),
    path('best_selling_product/', BestSellingProduct.as_view(), name='best_selling_product'),
    path('brand_landing/<str:brand_name>', BrandProduct.as_view(), name='brand_landing'),
    path('special_offers/<slug:slug>/', SpecialOffer.as_view(), name='special_category_list'),
]

apis_urlpatterns = [
    path('product_list/', ProductListApi.as_view(), name='product_list_api'),
    path('product/<slug:slug>/', ProductDetailApi.as_view(), name='product_detail_api'),
    path('category/<slug:slug>/', CategoryRelatedProductApi.as_view(), name='category_related_products_api'),
    path('discount/', DiscountedProductApi.as_view(), name='discounted_products_api'),
    path('best/products/', BestSellingProductApi.as_view(), name='best_selling_products_api'),
    path('brand/products/<str:brand_name>/', BrandProductApi.as_view(), name='brand_products_api'),
    path('product_detail/<slug:slug>/', SpecialOfferProductApi.as_view(), name='special_offer_products_api'),
]

urlpatterns = [
    *django_urlpatterns,
    *apis_urlpatterns,
]
