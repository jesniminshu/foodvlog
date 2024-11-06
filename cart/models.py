from django.db import models
from shop.models import *
from django.contrib.auth.models import User

# Create your models here.
class cartlist(models.Model):
    cart_id=models.CharField(max_length=250) 
    date_added=models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.cart_id
 
class items(models.Model):
    prodt=models.ForeignKey(products,on_delete=models.CASCADE)
    cart=models.ForeignKey(cartlist,on_delete=models.CASCADE)
    quantity=models.IntegerField()
    active=models.BooleanField(default=True)

    def __str__(self):
        return self.prodt

    def total(self):
        return self.prodt.price*self.quantity

class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    shipping_address = models.CharField(max_length=255)
    city = models.CharField(max_length=50)
    state = models.CharField(max_length=50)
    zip_code = models.CharField(max_length=10)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    date_ordered = models.DateTimeField(auto_now_add=True)
    completed = models.BooleanField(default=False)

    def __str__(self):
        return f"Order {self.id} by {self.user.username}"

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="items")
    product = models.ForeignKey(products, on_delete=models.CASCADE)
    quantity = models.IntegerField()

    def __str__(self):
        return f"{self.product.name} (x{self.quantity})"
