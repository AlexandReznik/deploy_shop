# Generated by Django 4.1.4 on 2023-04-13 10:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mainapp', '0018_product_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='image',
            field=models.ImageField(default='products/default_product.png', upload_to='products/'),
        ),
    ]
