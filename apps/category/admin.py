from django.contrib import admin
from .models import Category, SubCategory, SubSubCategory, ProductTag

admin.site.register(Category)
admin.site.register(SubCategory)
admin.site.register(SubSubCategory)


class ProductTagAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ('title',)}

admin.site.register(ProductTag, ProductTagAdmin)
