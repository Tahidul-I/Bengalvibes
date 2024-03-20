from django.db import models
import os

class SiteInfo(models.Model):
    facebook = models.URLField(max_length=200, null=True, blank=True)
    instagram = models.URLField(max_length=200, null=True, blank=True)
    pinterest = models.URLField(max_length=200, null=True, blank=True)
    twitter = models.URLField(max_length=200, null=True, blank=True)
    youtube = models.URLField(max_length=200, null=True, blank=True)
    phone_number = models.CharField(max_length=20, null=True, blank=True)
    email = models.EmailField(null=True, blank=True)
    location = models.CharField(max_length=255, null=True, blank=True)
    logo = models.ImageField(upload_to='uploads/core', null=True, blank=True)
    nav_background = models.ImageField(upload_to='uploads/core', null=True, blank=True)
    new_arrival_banner = models.ImageField(upload_to='uploads/core', null=True, blank=True)
    best_seller_banner = models.ImageField(upload_to='uploads/core', null=True, blank=True)
    featured_banner = models.ImageField(upload_to='uploads/core', null=True, blank=True)
    welcome_message = models.CharField(max_length=50, null=True, blank=True)
    title_fav_icon = models.ImageField(upload_to='uploads/site_settings', null=True, blank=True)

    @classmethod
    def get_site_info(cls):
        # There should be only one instance, so either return it or create a new one
        instance, created = cls.objects.get_or_create(pk=1)
        return instance

    def save(self, *args, **kwargs):
        # Set the primary key to 1 to ensure only one instance can exist
        self.pk = 1
        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        # Delete associated image files before deleting the object
        self.delete_images()
        super().delete(*args, **kwargs)

    def delete_images(self):
        # Delete associated image files from the filesystem
        for field in self._meta.fields:
            if isinstance(field, models.ImageField):
                file_path = getattr(self, field.name).path
                if file_path and os.path.exists(file_path):
                    os.remove(file_path)

    def __str__(self):
        return "Site Information"
