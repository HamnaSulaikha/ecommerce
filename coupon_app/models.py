from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

# Create your models here.

class Coupon(models.Model):
    code = models.CharField(max_length=20, unique=True)
    discount_percent = models.PositiveIntegerField(default=0)
    max_usage_count = models.PositiveIntegerField(default=1)
    current_usage_count = models.PositiveIntegerField(default=0)
    valid_from = models.DateTimeField()
    valid_to = models.DateTimeField()

    def is_valid(self):
        now = timezone.now()
        return self.valid_from <= now <= self.valid_to and self.current_usage_count < self.max_usage_count
    
class UsedCoupon(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    coupon = models.ForeignKey(Coupon, on_delete=models.CASCADE)
    order_id = models.PositiveIntegerField()
    usage_date = models.DateTimeField(auto_now_add=True)