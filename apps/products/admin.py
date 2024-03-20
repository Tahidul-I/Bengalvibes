from django.contrib import admin
from .models import *
# Register your models here.

# admin.site.register(Product)
admin.site.register(Color)
admin.site.register(Size)
admin.site.register(ProductVariation)
# admin.site.register(ProductImage)


class ProductImageInline(admin.StackedInline):
    model = ProductImage
    extra = 1  # Number of empty forms to display

class ProductVariationInline(admin.StackedInline):
    model = ProductVariation
    extra = 1  # Number of empty forms to display


class ProductAdmin(admin.ModelAdmin):
    inlines = [ProductImageInline,ProductVariationInline]

admin.site.register(Product, ProductAdmin)


