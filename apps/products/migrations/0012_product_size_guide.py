# Generated by Django 5.0 on 2024-02-05 10:00

import ckeditor.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0011_product_best_seller'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='size_guide',
            field=ckeditor.fields.RichTextField(default=1),
            preserve_default=False,
        ),
    ]
