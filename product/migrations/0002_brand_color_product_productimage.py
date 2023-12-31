# Generated by Django 3.2.23 on 2023-11-26 05:13

import ckeditor.fields
import colorfield.fields
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Brand',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('slug', models.SlugField(unique=True)),
            ],
            options={
                'verbose_name': 'Brand',
                'verbose_name_plural': 'Brand',
                'ordering': ('name',),
            },
        ),
        migrations.CreateModel(
            name='Color',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('color_code', colorfield.fields.ColorField(default='#FF0000', image_field=None, max_length=25, samples=None)),
            ],
            options={
                'verbose_name': 'Color',
                'verbose_name_plural': 'Colors',
                'ordering': ('name',),
            },
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=500)),
                ('slug', models.SlugField(max_length=500)),
                ('product_code', models.CharField(blank=True, max_length=100, null=True, unique=True)),
                ('sku', models.SlugField(blank=True, max_length=100, null=True, unique=True)),
                ('rating', models.PositiveIntegerField(default=5, validators=[django.core.validators.MaxValueValidator(5)], verbose_name='Product Rating(max:5)')),
                ('image', models.ImageField(upload_to='products/')),
                ('big_sale', models.ImageField(blank=True, null=True, upload_to='products/')),
                ('price', models.IntegerField()),
                ('discount', models.IntegerField()),
                ('product_information', ckeditor.fields.RichTextField(blank=True, null=True)),
                ('model_name', models.CharField(blank=True, max_length=250, null=True)),
                ('first_available_date', models.DateField(blank=True, null=True)),
                ('tags', models.CharField(blank=True, max_length=250, null=True)),
                ('description', ckeditor.fields.RichTextField(blank=True, null=True)),
                ('is_popular', models.BooleanField(default=False)),
                ('is_new_arrival', models.BooleanField(default=True)),
                ('is_best_seller', models.BooleanField(default=True)),
                ('is_our_product', models.BooleanField(default=False)),
                ('is_new_product', models.BooleanField(default=True)),
                ('is_hot_deal', models.BooleanField(default=True)),
                ('background_color', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='product.color')),
                ('brands', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='product.brand')),
                ('categories', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='product.category')),
            ],
            options={
                'verbose_name': 'Product',
                'verbose_name_plural': 'Products',
                'ordering': ['id'],
            },
        ),
        migrations.CreateModel(
            name='ProductImage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(upload_to='products/')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='product.product')),
            ],
            options={
                'verbose_name': 'Product Image',
                'verbose_name_plural': 'Product Images',
                'ordering': ('product',),
            },
        ),
    ]
