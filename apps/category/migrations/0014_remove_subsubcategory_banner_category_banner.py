# Generated by Django 5.0 on 2024-01-13 08:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('category', '0013_alter_subcategory_slug'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='subsubcategory',
            name='banner',
        ),
        migrations.AddField(
            model_name='category',
            name='banner',
            field=models.ImageField(default=1, upload_to='uploads/category_banner'),
            preserve_default=False,
        ),
    ]
