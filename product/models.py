from django.db import models
from django.core.validators import MaxValueValidator
from ckeditor.fields import RichTextField
from django.urls import reverse
from colorfield.fields import ColorField


# Create your models here.
class Color(models.Model):
    name = models.CharField(max_length=255)
    color_code = ColorField(default='#FF0000')

    class Meta:
        verbose_name = ("Color")
        verbose_name_plural = ("Colors")
        ordering = ("name",)

    def __str__(self):
        return str(self.name)
    
class Brand(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField(unique=True)

    class Meta:
        verbose_name = ("Brand")
        verbose_name_plural = ("Brand")
        ordering = ("name",)

    def get_products(self):
        return Product.objects.filter(brands=self)

    def __str__(self):
        return str(self.name)
    

class Slider(models.Model):
    image = models.ImageField(upload_to="slider/")
    discount = models.IntegerField()
    brand_name = models.CharField(max_length=250)
    slug = models.SlugField(unique=True)
    price = models.IntegerField()

    class Meta:
        verbose_name = ('Slider')
        verbose_name_plural = ('Sliders')

    def __str__(self):
        return str(self.brand_name)
    

class Category(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField(unique=True)
    image = models.ImageField(upload_to="categories/",blank=True,null=True)

    class Meta:
        verbose_name = ('Category')
        verbose_name_plural = ('Categorys')

    def get_products(self):
        return Product.objects.filter(categories=self)

    def __str__(self):
        return f"{self.name}"
    

class Product(models.Model):
    categories = models.ForeignKey(Category,on_delete=models.CASCADE, blank=True, null=True)
    brands = models.ForeignKey(Brand,on_delete=models.CASCADE, blank=True, null=True)
    name = models.CharField(max_length=500)     
    slug = models.SlugField(max_length=500)
    product_code = models.CharField(max_length=100, blank=True, null=True, unique=True)
    sku = models.SlugField(max_length=100, blank=True, null=True, unique=True)
    rating = models.PositiveIntegerField(
        validators=[MaxValueValidator(5)],
        default=5,
        verbose_name="Product Rating(max:5)",
    )
    image = models.ImageField(upload_to="products/")
    background_color = models.ForeignKey(Color,on_delete=models.CASCADE, blank=True, null=True)
    price = models.IntegerField()
    discount = models.IntegerField()
    product_information = RichTextField(blank=True, null=True)
    model_name = models.CharField(max_length=250,blank=True, null=True)
    first_available_date = models.DateField(blank=True, null=True)
    tags = models.CharField(max_length=250, blank=True, null=True)
    description = RichTextField(blank=True, null=True)
    is_popular = models.BooleanField(default=False)
    is_new_arrival = models.BooleanField(default=True)
    is_best_seller = models.BooleanField(default=True)
    is_our_product = models.BooleanField(default=False)
    is_new_product = models.BooleanField(default=True)
    is_hot_deal = models.BooleanField(default=True)

    class Meta:
        ordering = [
            "id",
        ]
        verbose_name = "Product"
        verbose_name_plural = "Products"

    def get_absolute_url(self):
        return reverse("product:shop_details", kwargs={"slug": self.slug})
    
    def related_products(self):
        return Product.objects.filter().exclude(pk=self.pk).distinct()[0:12]
    
    def get_big_sale(self):
        return ProductBig_Sale.objects.filter(product=self)

    def __str__(self):
        return self.name
    

class ProductImage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    image = models.ImageField(upload_to="products/")

    class Meta:
        verbose_name = "Product Image"
        verbose_name_plural = "Product Images"
        ordering = "product",


class ProductBig_Sale(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    image = models.ImageField(upload_to="products/")

    class Meta:
        verbose_name = "Product Big Sale"
        verbose_name_plural = "Product Big Sales"
        ordering = "product",
