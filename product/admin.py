from django.contrib import admin

# Register your models here.

from django.contrib import admin
from .models import (
    MainCategory,
    Banner,
    Product,
    ImageProduct,
    Color,
    IpAddress,
    ColorProduct,
    Brand,
    SizeProduct,
    Size,
    DiscountProduct,
    Specification,
    )
from django.utils.translation import gettext as _


class MainCategoryAdmin(admin.ModelAdmin):
    list_display=['title','slug','parent']
    list_filter=['title']
    search_fields=['title','slug','description']

class BannerAdmin(admin.ModelAdmin):
    list_display=['title','slug']
    list_filter=['title']
    search_fields=['title','slug','description']

class ImageProductAdmin(admin.StackedInline):
    model = ImageProduct

class ColorProductAdmin(admin.TabularInline):
    model = ColorProduct

class SizeProductAdmin(admin.TabularInline):
    model = SizeProduct

class SpecificationAdmin(admin.TabularInline):
    model = Specification
    
class ProductAdmin(admin.ModelAdmin):
    list_display=['title','status','number_of_visits','cal_discount']
    list_filter=['slug','main_category',]
    search_fields=['category','slug']
    ordering=['-updated']
    inlines = [SpecificationAdmin,ImageProductAdmin,ColorProductAdmin,SizeProductAdmin]   
    readonly_fields=['number_of_visits','cal_discount']

class ColorAdmin(admin.ModelAdmin):
    list_display=['color_pic']
    list_filter=['name']
    search_fields=['name']

class BrandAdmin(admin.ModelAdmin):
    list_display=["display_logo"]



admin.site.register(MainCategory,MainCategoryAdmin)
admin.site.register(SpecialCategory,SpecialCategoryAdmin)
admin.site.register(Product,ProductAdmin)
admin.site.register(Color,ColorAdmin)
admin.site.register(Brand,BrandAdmin)
admin.site.register(Size)
admin.site.register(DiscountProduct)
admin.site.register(IpAddress)


