from django.db import models
from django.forms import ValidationError
from ..products.models import Product
import os
# Create your models here.

class Banner(models.Model):
    image = models.ImageField(upload_to='uploads/banner', height_field=None, width_field=None, max_length=None)
    
    def __str__(self):
        return self.image.url

    def delete(self, *args, **kwargs):
        # Delete the associated banner image file from the filesystem
        if self.image:
            # Get the file path
            file_path = self.image.path
            # Check if the file exists
            if os.path.exists(file_path):
                # If it exists, delete the file
                os.remove(file_path)
        # Call the superclass delete method to delete the object from the database
        super().delete(*args, **kwargs)
    

class VideoAdvertisement(models.Model):
    video = models.FileField(upload_to='uploads/video_ad', max_length=100)
    caption = models.CharField(max_length=50)

    def __str__(self):
        return self.video.url

    def delete(self, *args, **kwargs):
        # Delete the associated video file from the filesystem
        if self.video:
            # Get the file path
            file_path = self.video.path
            # Check if the file exists
            if os.path.exists(file_path):
                # If it exists, delete the file
                os.remove(file_path)
        # Call the superclass delete method to delete the object from the database
        super().delete(*args, **kwargs)


class VerticalBannerProudctAdvertisement(models.Model):
    POSITION_CHOICES = [
        ('left', 'Left'),
        ('right', 'Right'),
    ]
    title = models.CharField(max_length=50)
    banner = models.ImageField(upload_to='uploads/verticalbanner')
    url = models.URLField()
    products = models.ManyToManyField(Product, related_name='vertical_banners_product')
    position = models.CharField(max_length=5, choices=POSITION_CHOICES)

    def __str__(self):
        return self.title

    def delete(self, *args, **kwargs):
        # Delete the associated banner image file from the filesystem
        if self.banner:
            # Get the file path
            file_path = self.banner.path
            # Check if the file exists
            if os.path.exists(file_path):
                # If it exists, delete the file
                os.remove(file_path)
        # Call the superclass delete method to delete the object from the database
        super().delete(*args, **kwargs)

    

class VerticalBannerAdvertisement(models.Model):
    title = models.CharField(max_length=50)
    image = models.ImageField(upload_to='uploads/verticalad')
    url = models.URLField(max_length=200)

    def __str__(self):
        return self.title

    def delete(self, *args, **kwargs):
        # Delete the associated vertical banner image file from the filesystem
        if self.image:
            # Get the file path
            file_path = self.image.path
            # Check if the file exists
            if os.path.exists(file_path):
                # If it exists, delete the file
                os.remove(file_path)
        # Call the superclass delete method to delete the object from the database
        super().delete(*args, **kwargs)
    
