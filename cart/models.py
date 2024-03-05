from django.db import models
from django.contrib.auth.models import User
from store.models import Variant
from decimal import Decimal


# Create your models here.

class CartItem(models.Model):
    product_variant = models.ForeignKey(Variant, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def subtotal(self):
        return self.product_variant.price * self.quantity

    def __str__(self):
        return f"{self.product_variant.product.name} - {self.product_variant.color} - {self.quantity} units"
    

class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    items = models.ManyToManyField(CartItem, related_name='cart_items')
    total_price = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    def update_total_price(self):
        self.total_price = sum(item.subtotal() for item in self.items.all())
        self.save()

class UserCart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Variant, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    title = models.TextField(default=1)
    timestamp = models.DateTimeField(auto_now_add=True)
    is_checkout_done =models.BooleanField(default=False)
    
    @property
    def sub_total(self):
        return Decimal(self.quantity) * self.product.price

    def __str__(self):
        return self.title