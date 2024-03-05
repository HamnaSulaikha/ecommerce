from django.db import models
from store.models import Address
from django.contrib.auth.models import User
from cart.models import UserCart
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone

# Create your models here.
class Order(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    cart_items = models.ManyToManyField(UserCart, related_name='order_cart_items')
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    order_date = models.DateTimeField(auto_now_add=True)
    payment_status = models.CharField(max_length=20, choices=[('Pending', 'Pending'), ('Paid', 'Paid')], default='Pending')
    delivery_status = models.CharField(max_length=20, choices=[('Pending', 'Pending'), ('Shipped', 'Shipped'), ('Delivered', 'Delivered'), ('Cancelled', 'Cancelled')], default='Pending')
    payment_type = models.CharField(max_length=20, choices=[('Credit Card', 'Credit Card'), ('Cash on Delivery', 'Cash on Delivery'),('UPI', 'UPI')])
    shipping_address = models.ForeignKey(Address, on_delete=models.SET_NULL, null=True, blank=True)
    delivered_date = models.DateTimeField(null=True, blank=True)

    def update_delivered_date(self):
        if self.delivery_status == 'Delivered' and not self.delivered_date:
            self.delivered_date = timezone.now()
            self.save()

    def __str__(self):
        return f"Order #{self.id} - {self.user.username}" 
    
# Signal to automatically update delivered date when an order is saved
@receiver(post_save, sender=Order)
def update_delivered_date(sender, instance, **kwargs):
    instance.update_delivered_date()