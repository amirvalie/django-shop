from rest_framework import serializers
from ..models import Product
from ...categories.models import Category
from django.contrib.auth import get_user_model
User = get_user_model()


class ProductSerializer(serializers.ModelSerializer):
    user = serializers.SlugRelatedField(queryset=User.objects.all(), slug_field='phone')
    category = serializers.SlugRelatedField(many=True, queryset=Category.objects.all(), slug_field='slug')

    class Meta:
        model = Product
        fields = [
            'user',
            'title',
            'slug',
            'category',
            'banner',
            'brand',
            'introduction',
            'price',
            'discount_product',
            'thumbnail',
            'quantity',
            'available',
            'sales_number',
        ]


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = [
            'title',
            'slug',
            'status',
            'thumbnail',
            'parent',
        ]
