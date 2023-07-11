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
    CategoryDetailUpdateAPi,
    CategoryListCreateAPi,
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
    path('api/products/search/', ProductListApi.as_view(), name='product_list_api'),
    path('api/product/<slug:slug>/', ProductDetailApi.as_view(), name='product_detail_api'),
    path('api/products/category/<slug:category_slug>/', CategoryRelatedProductApi.as_view(), name='category_related_products_api'),
    path('api/products/discount/', DiscountedProductApi.as_view(), name='discounted_products_api'),
    path('api/products/best-selling/', BestSellingProductApi.as_view(), name='best_selling_products_api'),
    path('api/products/brand/<str:brand_name>/', BrandProductApi.as_view(), name='brand_products_api'),
    path('api/products/offer/<slug:offer_slug>/', SpecialOfferProductApi.as_view(), name='special_offer_products_api'),
    path('api/category/<slug:slug>/', CategoryDetailUpdateAPi.as_view(), name='category_detail_put_api'),
    path('api/category/', CategoryListCreateAPi.as_view(), name='category_list_create_api'),
]

urlpatterns = [
    *django_urlpatterns,
    *apis_urlpatterns,
]
