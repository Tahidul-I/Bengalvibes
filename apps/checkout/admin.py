from django.contrib import admin
from .models import Order, OrderItem

# Register Order model
@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['tracking_no']
    search_fields = ['tracking_no']
    readonly_fields = ['user','first_name','last_name','city','address','postal_code','phone','email','message','total_price','payment_mode','payment_id','tracking_no','created_at','updated_at','created_at','updated_at']

# Register OrderItem model
@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ['id', 'order', 'product', 'price', 'quantity']
    search_fields = ['order__tracking_no', 'product__title']
    readonly_fields = ['order', 'product', 'price', 'quantity']

