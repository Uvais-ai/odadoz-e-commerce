from django.db import models
from django.contrib.auth.models import User
from product.models import Product

# Create your models here.
class Order(models.Model):  
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    firstname=models.CharField(max_length=250)
    lastname=models.CharField(max_length=250)
    district=models.CharField(max_length=250)
    address=models.TextField()
    town=models.CharField(max_length=350)
    country=models.CharField(max_length=350)
    postcode=models.IntegerField()
    email=models.EmailField(max_length=350)
    telephone=models.IntegerField()

    verbose_name = "Order"
    verbose_name_plural = "Orders"


    def __str__(self):
        return self.firstname
    
class Order_Item(models.Model):
    order=models.ForeignKey(Order,on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    image=models.ImageField(upload_to='media/order_image')
    product_name = models.CharField(max_length=450) 
    price=models.FloatField()
    quantity=models.IntegerField()
    total=models.IntegerField()
    paid=models.BooleanField(default=False)

    verbose_name = "Order Item"
    verbose_name_plural = "Order Items"

    def __str__(self):
        return self.product_name
    
    
class Wishlist(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey("product.Product", on_delete=models.CASCADE)
    variant = models.CharField(max_length=100)
    price = models.PositiveIntegerField()

    class Meta:
        unique_together = ("user", "product")
        verbose_name = "Wishlist Item"
        verbose_name_plural = "Wishlist Items"