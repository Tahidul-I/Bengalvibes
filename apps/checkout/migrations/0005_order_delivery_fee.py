# Generated by Django 5.0.2 on 2024-03-07 08:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('checkout', '0004_order_payment_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='delivery_fee',
            field=models.FloatField(default=1),
            preserve_default=False,
        ),
    ]
