# Generated by Django 3.2.11 on 2022-03-28 10:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='product',
            name='related_products',
        ),
        migrations.AddField(
            model_name='product',
            name='main_image',
            field=models.ImageField(blank=True, help_text='Upload a product image', upload_to='static/product_module/product'),
        ),
    ]
