from django.contrib import admin
from .models import Category,Product,Variant,ProductImage,UserProfile,Address

# Register your models here.
admin.site.register(UserProfile)
admin.site.register(Category)
admin.site.register(Product)
admin.site.register(Address)
admin.site.register(Variant)
admin.site.register(ProductImage)











