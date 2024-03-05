from django import forms
from .models import Coupon


class DateInput(forms.DateInput):
    input_type = 'date'



class CouponForm(forms.ModelForm):
    class Meta:
        model = Coupon
        fields = '__all__'

        widgets = {
            'valid_from' : DateInput(),
            'valid_to' : DateInput(),
        }