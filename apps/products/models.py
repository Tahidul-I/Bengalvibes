from django.db import models
from ..category.models import SubSubCategory,SubCategory
from ..category.models import ProductTag
from django.utils.text import slugify
from ckeditor.fields import RichTextField
import os

class Product(models.Model):
    subcategory = models.ForeignKey(SubCategory, related_name=("product_subcategory"), on_delete=models.CASCADE)
    subsubcategory_tag = models.ForeignKey(SubSubCategory, related_name=("subsubcategory"), on_delete=models.CASCADE,blank=True,null=True)
    title = models.CharField(max_length=150)
    product_code = models.CharField(max_length=50)
    slug = models.SlugField(max_length=255, unique=True, blank=True, null=True)
    original_price = models.IntegerField(blank=True, null=True)
    selling_price = models.IntegerField()
    image = models.ImageField(upload_to='uploads/product', height_field=None, width_field=None, max_length=None)
    short_description = models.CharField(max_length=50)
    description = RichTextField()
    is_featured = models.BooleanField(default=False)
    new_arrival = models.BooleanField(default=False)
    best_seller = models.BooleanField(default=False)
    size_guide = RichTextField()
    tag = models.ManyToManyField(ProductTag)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        # Delete associated images before deleting the object
        self.delete_images()
        super().delete(*args, **kwargs)

    def delete_images(self):
        # Delete associated image files from the filesystem
        if self.image:
            file_path = self.image.path
            if file_path and os.path.exists(file_path):
                os.remove(file_path)

    def __str__(self):
        return self.product_code

class Color(models.Model):
    title = models.CharField(max_length=50)
    color_code = models.CharField(max_length=10)
    
    def __str__(self):
        return self.title

class Size(models.Model):
    title = models.CharField(max_length=50)
    size = models.CharField(max_length=10)
    
    def __str__(self):
        return self.title

class ProductVariation(models.Model):
    product = models.ForeignKey(Product, related_name=("product"), on_delete=models.CASCADE)
    color = models.ForeignKey(Color, related_name=("product_variation_color"), on_delete=models.CASCADE)
    size = models.ForeignKey(Size, related_name=("product_variation_size"), on_delete=models.CASCADE)
    quantity = models.IntegerField()
    selling_price = models.IntegerField()

    def __str__(self):
        return f"{self.product.product_code} - {self.color.title} - {self.size.title}"
    
    class Meta:
        # Ensure uniqueness based on the combination of product, color, and size
        unique_together = ('product', 'color', 'size')

    def delete(self, *args, **kwargs):
        # No images to delete in ProductVariation
        super().delete(*args, **kwargs)

class ProductImage(models.Model):
    product = models.ForeignKey(Product, related_name='product_images', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='uploads/productVariation', height_field=None, width_field=None, max_length=None)    
    
    def __str__(self):
        return f"Image for {self.product.product_code}"

    def delete(self, *args, **kwargs):
        # Delete associated image file from the filesystem
        if self.image:
            file_path = self.image.path
            if file_path and os.path.exists(file_path):
                os.remove(file_path)
        super().delete(*args, **kwargs)


