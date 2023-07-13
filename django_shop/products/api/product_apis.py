from rest_framework.views import APIView
from ...api.pagination import LimitOffsetPagination
from rest_framework import status
from rest_framework.response import Response
from drf_spectacular.utils import extend_schema
from rest_framework import serializers
from .serializers import ProductSerializer, CategorySerializer
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
from rest_framework.permissions import IsAuthenticated, AllowAny, IsAdminUser


class ProductListApi(APIView):
    pagination_class = LimitOffsetPagination
    permission_classes = [AllowAny]

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
    permission_classes = [AllowAny]

    @extend_schema(request=ProductSerializer)
    def get(self, request, slug, *args, **kwargs):
        product_object = get_product(slug=slug)
        serializer = ProductSerializer(product_object, context={'request': request})
        return Response(
            serializer.data, status=status.HTTP_200_OK
        )


class CategoryDetailUpdateAPi(APIView):
    def get_permissions(self):
        if self.request.method == 'GET':
            self.permission_classes = [AllowAny]
        else:
            self.permission_classes = [IsAdminUser]
        return super(self.__class__, self).get_permissions()

    @extend_schema(responses=CategorySerializer)
    def get(self, request, slug, *args, **kwargs):
        try:
            category_object = get_category(slug=slug)
        except ObjectDoesNotExist:
            return Response(
                {"Doesn't exist": "Category matching query does not exist."},
                status=status.HTTP_404_NOT_FOUND
            )
        serializer = CategorySerializer(category_object)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @extend_schema(request=CategorySerializer, responses=CategorySerializer)
    def put(self, request, slug, *args, **kwargs):
        try:
            instance = get_category(slug=slug)
        except ObjectDoesNotExist:
            return Response(
                {"Doesn't exist": f"Category with {slug} doesn't exist"},
                status=status.HTTP_404_NOT_FOUND
            )
        serializer = CategorySerializer(instance, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class CategoryListCreateAPi(APIView):
    def get_permissions(self):
        if self.request.method == 'GET':
            self.permission_classes = [AllowAny]
        else:
            self.permission_classes = [IsAdminUser]
        return super(self.__class__, self).get_permissions()

    @extend_schema(responses=CategorySerializer)
    def get(self, request, *args, **kwargs):
        queryset = category_list()
        serializer = CategorySerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @extend_schema(request=CategorySerializer, responses=CategorySerializer)
    def post(self, request, *args, **kwargs):
        serializer = CategorySerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class CategoryRelatedProductApi(APIView):
    pagination_class = LimitOffsetPagination
    permission_classes = [AllowAny]

    @extend_schema(request=ProductSerializer)
    def get(self, request, category_slug, *args, **kwargs):
        products = category_products(slug=category_slug)
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class SpecialOfferProductApi(APIView):
    pagination_class = LimitOffsetPagination
    permission_classes = [AllowAny]

    @extend_schema(request=ProductSerializer)
    def get(self, request, offer_slug, *args, **kwargs):
        products = special_offers(slug=offer_slug)
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class DiscountedProductApi(APIView):
    pagination_class = LimitOffsetPagination
    permission_classes = [AllowAny]

    @extend_schema(request=ProductSerializer)
    def get(self, request, *args, **kwargs):
        products = discounted_products()
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class BestSellingProductApi(APIView):
    pagination_class = LimitOffsetPagination
    permission_classes = [AllowAny]

    @extend_schema(request=ProductSerializer)
    def get(self, request, *args, **kwargs):
        products = best_selling_products()
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class BrandProductApi(APIView):
    pagination_class = LimitOffsetPagination
    permission_classes = [AllowAny]

    @extend_schema(request=ProductSerializer)
    def get(self, request, brand_name, *args, **kwargs):
        products = brand_products(brand_name=brand_name)
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)