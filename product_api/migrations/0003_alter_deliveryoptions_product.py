# Generated by Django 4.1.1 on 2022-10-03 22:21

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('product_api', '0002_alter_product_seller_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='deliveryoptions',
            name='product',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='delivery_options', related_query_name='delivery_options', to='product_api.product'),
        ),
    ]
