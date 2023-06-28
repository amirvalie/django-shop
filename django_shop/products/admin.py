from django.contrib import admin

# Register your models here.

from django.contrib import admin
from .models import (
    Product,
    ProductImage,
    Color,
    IpAddress,
    ProductColor,
    Brand,
    ProductSize,
    Size,
    DiscountProduct,
    Specification,
)
from django.utils.translation import gettext as _


class ProductImageAdmin(admin.StackedInline):
    model = ProductImage


class ProductColorAdmin(admin.TabularInline):
    model = ProductColor


class ProductSizeAdmin(admin.TabularInline):
    model = ProductSize


class SpecificationAdmin(admin.TabularInline):
    model = Specification


class ProductAdmin(admin.ModelAdmin):
    list_display = ['title', 'status', 'cal_discount']
    list_filter = ['slug', ]
    search_fields = ['category', 'slug']
    ordering = ['-updated']
    inlines = [SpecificationAdmin, ProductImageAdmin, ProductColorAdmin, ProductSizeAdmin]
    readonly_fields = ['cal_discount']


class ColorAdmin(admin.ModelAdmin):
    list_display = ['color_pic']
    list_filter = ['name']
    search_fields = ['name']


class BrandAdmin(admin.ModelAdmin):
    list_display = ["display_logo"]


admin.site.register(Product, ProductAdmin)
admin.site.register(Color, ColorAdmin)
admin.site.register(Brand, BrandAdmin)
admin.site.register(Size)
admin.site.register(DiscountProduct)
admin.site.register(IpAddress)
