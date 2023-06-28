from rest_framework.views import APIView
from ...api.mixins import ApiAuthMixin
from ...api.pagination import LimitOffsetPagination
from ..blogic.selectors import product_list, get_product, special_offers, discounted_products, best_selling_products, \
    brand_products, get_response_paginator
from .serializers import ProductSerializer
from rest_framework import status
from rest_framework.response import Response
from drf_spectacular.utils import extend_schema
from rest_framework import serializers
from rest_framework.generics import ListAPIView
from ..blogic.selectors import category_products


class ProductListApi(APIView):
    pagination_class = LimitOffsetPagination

    class FilterSerializer(serializers.Serializer):
        title = serializers.CharField(max_length=100)

    @extend_schema(request=ProductSerializer)
    def get(self, request, *args, **kwargs):
        filter_serializer = self.FilterSerializer(data=request.data)
        filter_serializer.is_valid(raise_exception=True)
        products = product_list(filters=filter_serializer.validated_data)
        return get_response_paginator(
            paginator_class=self.pagination_class,
            queryset=products,
            serializers_class=ProductSerializer,
            request=request,
            view=self,
        )


class ProductDetailApi(ApiAuthMixin, APIView):
    @extend_schema(request=ProductSerializer)
    def get(self, request, slug, *args, **kwargs):
        product_object = get_product(slug=slug)
        serializer = ProductSerializer(product_object)
        return Response(
            serializer.data, status=status.HTTP_200_OK
        )


class CategoryRelatedProductApi(ApiAuthMixin, APIView):
    pagination_class = LimitOffsetPagination

    def get(self, request, slug, *args, **kwargs):
        products = category_products(slug=slug)
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class SpecialOfferProductApi(ApiAuthMixin, APIView):
    pagination_class = LimitOffsetPagination

    def get(self, request, slug, *args, **kwargs):
        products = special_offers(slug=slug)
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class DiscountedProductApi(ApiAuthMixin, APIView):
    pagination_class = LimitOffsetPagination

    def get(self, request, *args, **kwargs):
        products = discounted_products()
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class BestSellingProductApi(ApiAuthMixin, APIView):
    pagination_class = LimitOffsetPagination

    def get(self, request, *args, **kwargs):
        products = best_selling_products()
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class BrandProductApi(ApiAuthMixin, APIView):
    pagination_class = LimitOffsetPagination

    def get(self, request, brand_name, *args, **kwargs):
        products = brand_products(brand_name=brand_name)
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

