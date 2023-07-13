from rest_framework import serializers, permissions
from ..models import Product
from ...categories.models import Category
from django.contrib.auth import get_user_model

User = get_user_model()


class ProductSerializer(serializers.ModelSerializer):
    def __init__(self, *args, **kwargs):
        # Instantiate the superclass normally
        super(ProductSerializer, self).__init__(*args, **kwargs)
        request = kwargs.get('context').get('request')
        if not request.user.is_staff:
            not_allowed_fields = ['user', 'discount_product', 'quantity', 'sales_number']
            for not_allowed_field in not_allowed_fields:
                self.fields.pop(not_allowed_field)

    user = serializers.SlugRelatedField(queryset=User.objects.all(), slug_field='phone')
    category = serializers.SlugRelatedField(many=True, queryset=Category.objects.all(), slug_field='slug')
    discount_product = serializers.CharField()

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
