from django import forms
from store.models import Variant,Product


class VariantForm(forms.ModelForm):
    class Meta:
        model = Variant
        fields = ['color', 'stock', 'price_modifier', 'fittings', 'quality', 'features', 'is_available']



class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'description', 'category', 'price', 'rating', 'image', 'discount_percentage', 'brand', 'is_available']