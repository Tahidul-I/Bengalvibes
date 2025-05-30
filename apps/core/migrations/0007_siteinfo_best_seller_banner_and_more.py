# Generated by Django 5.0 on 2024-02-05 06:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0006_siteinfo_title_fav_icon'),
    ]

    operations = [
        migrations.AddField(
            model_name='siteinfo',
            name='best_seller_banner',
            field=models.ImageField(default=1, upload_to='uploads/core'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='siteinfo',
            name='new_arrival_banner',
            field=models.ImageField(default=1, upload_to='uploads/core'),
            preserve_default=False,
        ),
    ]
