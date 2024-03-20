from django.utils.safestring import mark_safe
from django.contrib import admin
from .models import *

class BannerAdmin(admin.ModelAdmin):
    list_display = ('display_image',)

    def display_image(self, obj):
        return mark_safe('<img src="{url}" width="{width}" height="{height}" />'.format(
            url=obj.image.url,
            width='500px',
            height='100px',
        ))
    
    display_image.short_description = 'Banner Items'

admin.site.register(Banner, BannerAdmin)

class VideoAdvertisementAdmin(admin.ModelAdmin):
    list_display = ('display_image',)

    def display_image(self, obj):
        return mark_safe('<video width="320" height="240" controls><source src="{url}" type="video/mp4"></video>'.format(
            url=obj.video.url,
            width='500px',
            height='100px',
        ))
    
    display_image.short_description = 'Advertisement Videos'

admin.site.register(VideoAdvertisement, VideoAdvertisementAdmin)
admin.site.register(VerticalBannerProudctAdvertisement)
admin.site.register(VerticalBannerAdvertisement)
