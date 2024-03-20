from django.db import models
from django.utils.text import slugify
import os

def delete_file(file_field):
    # Delete the associated file from the filesystem
    if file_field:
        # Get the file path
        file_path = file_field.path
        # Check if the file exists
        if os.path.exists(file_path):
            # If it exists, delete the file
            os.remove(file_path)

class Category(models.Model):
    title = models.CharField(max_length=50)
    slug = models.SlugField(max_length=255, unique=True, blank=True, null=True)
    icon = models.ImageField(upload_to='uploads/category_icon', height_field=None, width_field=None, max_length=None)
    banner = models.ImageField(upload_to='uploads/category_banner', height_field=None, width_field=None, max_length=None)
    is_featured = models.BooleanField()

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        delete_file(self.icon)
        delete_file(self.banner)
        super().delete(*args, **kwargs)

    def __str__(self):
        return self.title
    

class SubCategory(models.Model):
    category = models.ForeignKey(Category, related_name=("category"), on_delete=models.CASCADE)
    title = models.CharField(max_length=50)
    slug = models.SlugField(max_length=255, blank=True, null=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        super().delete(*args, **kwargs)

    def __str__(self):
        return  f"{self.category.title} > {self.title}"
    

class SubSubCategory(models.Model):
    subcategory = models.ForeignKey(SubCategory, related_name=("subcategory"), on_delete=models.CASCADE)
    title = models.CharField(max_length=50)
    slug = models.SlugField(max_length=255, blank=True, null=True)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        super().delete(*args, **kwargs)

    def __str__(self):
        return f"{self.subcategory.category.title} > {self.subcategory.title} > {self.title}"


class ProductTag(models.Model):
    title = models.CharField(max_length=50)
    slug = models.SlugField(null=True, blank=True)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title