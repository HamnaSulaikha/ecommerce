from django import forms
from orders.models import Order

class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['user',  'total_price', 'payment_status', 'delivery_status', 'payment_type', ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Customize form fields as needed:
        self.fields['user'].disabled = True
        self.fields['total_price'].disabled = True
        self.fields['payment_type'].disabled = True