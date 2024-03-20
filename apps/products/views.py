from django.http import JsonResponse
from django.shortcuts import render
from .models import Product, ProductVariation, ProductImage
# Create your views here.
def product_details(request, slug):
    product = Product.objects.get(slug=slug)
    product_images_all = ProductImage.objects.filter(product=product.id)
    colors = ProductVariation.objects.filter(product=product).values('color__id','color__title','color__color_code').distinct()
    sizes = ProductVariation.objects.filter(product=product).values('size__id','size__title','color_id', 'selling_price', 'size__size').distinct()

   
    product_subcategory = product.subcategory
    product_category = product_subcategory.category

    related_products = Product.objects.filter(subcategory__category=product_category).exclude(id=product.id)

    context = {'product':product, 'colors':colors, 'sizes':sizes, 'product_images_all':product_images_all, 'related_products':related_products}
    return render(request, 'product-details.html', context)


