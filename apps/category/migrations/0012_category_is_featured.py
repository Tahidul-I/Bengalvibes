# Generated by Django 5.0 on 2024-01-13 04:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('category', '0011_subsubcategory_banner'),
    ]

    operations = [
        migrations.AddField(
            model_name='category',
            name='is_featured',
            field=models.BooleanField(default=1),
            preserve_default=False,
        ),
    ]
