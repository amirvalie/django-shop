from django.contrib import admin
from .models import (
    Category,
    Banner,
)
# Register your models here.
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['title', 'slug', 'parent']
    list_filter = ['title']
    search_fields = ['title', 'slug', 'description']


class BannerAdmin(admin.ModelAdmin):
    list_display = ['title', 'slug']
    list_filter = ['title']
    search_fields = ['title', 'slug', 'description']


admin.site.register(Category,CategoryAdmin)
admin.site.register(Banner,BannerAdmin)
