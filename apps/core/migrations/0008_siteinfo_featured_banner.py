# Generated by Django 5.0 on 2024-02-05 06:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0007_siteinfo_best_seller_banner_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='siteinfo',
            name='featured_banner',
            field=models.ImageField(default=1, upload_to='uploads/core'),
            preserve_default=False,
        ),
    ]
