from rest_framework.views import APIView
from ...api.pagination import LimitOffsetPagination
from rest_framework import status
from rest_framework.response import Response
from drf_spectacular.utils import extend_schema
from rest_framework import serializers
from .serializers import ProductSerializer, CategorySeriaizer
from ...categories.models import Category
from ..blogic.selectors import (
    product_list,
    get_product,
    special_offers,
    discounted_products,
    best_selling_products,
    category_products,
    brand_products,
    get_response_paginator
)
from ...categories.blogic.selectors import get_category, category_list
from django.core.exceptions import ObjectDoesNotExist


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
            serializer_class=ProductSerializer,
            request=request,
            view=self,
        )


class ProductDetailApi(APIView):

    @extend_schema(request=ProductSerializer)
    def get(self, request, slug, *args, **kwargs):
        product_object = get_product(slug=slug)
        serializer = ProductSerializer(product_object, context={'request': request})
        return Response(
            serializer.data, status=status.HTTP_200_OK
        )


class CategoryDetailPutAPi(APIView):
    @extend_schema(responses=CategorySeriaizer)
    def get(self, request, slug, *args, **kwargs):
        try:
            category_object = get_category(slug=slug)
        except ObjectDoesNotExist:
            return Response(
                {"Doesn't exist": "Category matching query does not exist."},
                status=status.HTTP_404_NOT_FOUND
            )
        serializer = CategorySeriaizer(category_object)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @extend_schema(request=CategorySeriaizer, responses=CategorySeriaizer)
    def put(self, request, slug, *args, **kwargs):
        try:
            instance = get_category(slug=slug)
        except ObjectDoesNotExist:
            return Response(
                {"Doesn't exist": f"Category with {slug} doesn't exist"},
                status=status.HTTP_404_NOT_FOUND
            )
        serializer = CategorySeriaizer(instance, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class CategoryListCreateAPi(APIView):
    @extend_schema(responses=CategorySeriaizer)
    def get(self, request, *args, **kwargs):
        queryset = category_list()
        print(queryset)
        serializer = CategorySeriaizer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @extend_schema(request=CategorySeriaizer, responses=CategorySeriaizer)
    def post(self, request, *args, **kwargs):
        serializer = CategorySeriaizer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class CategoryRelatedProductApi(APIView):
    pagination_class = LimitOffsetPagination

    @extend_schema(request=ProductSerializer)
    def get(self, request, category_slug, *args, **kwargs):
        products = category_products(slug=category_slug)
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class SpecialOfferProductApi(APIView):
    pagination_class = LimitOffsetPagination

    @extend_schema(request=ProductSerializer)
    def get(self, request, offer_slug, *args, **kwargs):
        products = special_offers(slug=offer_slug)
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class DiscountedProductApi(APIView):
    pagination_class = LimitOffsetPagination

    @extend_schema(request=ProductSerializer)
    def get(self, request, *args, **kwargs):
        products = discounted_products()
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class BestSellingProductApi(APIView):
    pagination_class = LimitOffsetPagination

    @extend_schema(request=ProductSerializer)
    def get(self, request, *args, **kwargs):
        products = best_selling_products()
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class BrandProductApi(APIView):
    pagination_class = LimitOffsetPagination

    @extend_schema(request=ProductSerializer)
    def get(self, request, brand_name, *args, **kwargs):
        products = brand_products(brand_name=brand_name)
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
