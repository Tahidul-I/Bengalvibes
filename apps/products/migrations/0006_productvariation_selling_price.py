# Generated by Django 5.0 on 2023-12-19 04:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0005_productvariationimage_productvariation_images'),
    ]

    operations = [
        migrations.AddField(
            model_name='productvariation',
            name='selling_price',
            field=models.IntegerField(default=12333),
            preserve_default=False,
        ),
    ]
