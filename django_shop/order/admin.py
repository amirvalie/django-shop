from django.contrib import admin
from .models import Order,OrderItem,DatePikcer


class OrderItemInline(admin.StackedInline):
    model = OrderItem
    raw_id_fields = ['product']
    
@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['user','status','created', 'update_time']
    list_filter = ['created', 'updated']
    inlines = [OrderItemInline]


admin.site.register(DatePikcer)