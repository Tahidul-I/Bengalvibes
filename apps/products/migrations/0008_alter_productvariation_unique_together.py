# Generated by Django 5.0 on 2023-12-27 04:33

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0007_productimage_alter_productvariation_images_and_more'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='productvariation',
            unique_together={('product', 'color', 'size')},
        ),
    ]
