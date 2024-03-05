from django.db import models
from django.contrib.auth.models import User
import uuid
from audioop import reverse

# Create your models here.

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True,related_name="profile")
    phone = models.CharField(max_length=20)
    email = models.EmailField(null=True)
    age = models.IntegerField(null=True)
    wallet_balance = models.DecimalField(max_digits=10, decimal_places=2, default=0) 
    otp = models.CharField(max_length=100, null=True, blank=True)  
    
    def __str__(self):
        return self.phone
    
class Category(models.Model):
    name = models.CharField(max_length=255)
    image = models.ImageField(upload_to='category_images', null=True, blank=True)
    description = models.TextField(blank=True)  
    
    class Meta:
        verbose_name_plural = "Catogories"

    def __str__(self):
        return self.name
    
class Address(models.Model):
    street = models.CharField(max_length=100)
    city = models.CharField(max_length=50)
    state = models.CharField(max_length=50)
    zip_code = models.CharField(max_length=10)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

class Product(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE) 
    price = models.DecimalField(max_digits=10, decimal_places=2)
    rating = models.DecimalField(max_digits=3, decimal_places=1, default=0) 
    image = models.ImageField(upload_to='product_images',null=True) 
    discount_percentage = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    brand = models.CharField(max_length=100, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    is_available = models.BooleanField(default=True,null=True)
    
    def __str__(self):
        return self.name

class Variant(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    color = models.CharField(max_length=50)
    stock = models.IntegerField()
    price_modifier = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)
    discount_percentage = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2,default=500)

    fittings = models.CharField(max_length=50, null=True, blank=True)
    quality = models.CharField(max_length=50, null=True, blank=True)
    features = models.CharField(max_length=50, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True,null=True)
    is_available = models.BooleanField(default=True,null=True)
    image = models.ImageField(upload_to='variant_images',null=True)
    image2 = models.ImageField(upload_to='variant_images',null=True)
    image3 = models.ImageField(upload_to='variant_images',null=True)

    def __str__(self):
        return f"{self.product.name} - {self.color}"

class ProductImage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)  # Relationship to Product model
    image = models.ImageField(upload_to='product_images',null=True) 