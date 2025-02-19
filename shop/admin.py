from django.contrib import admin
from .models import Product, Order, OrderItem

admin.site.register(Product)

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['user', 'total_price', 'status', 'created_at']
    list_filter = ['status', 'created_at']

@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ['order', 'product', 'quantity', 'price']
