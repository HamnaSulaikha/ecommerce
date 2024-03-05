from pyexpat.errors import messages
from django.shortcuts import render,get_object_or_404, redirect
from django.views import View
from .models import Coupon
from coupon_app.forms import CouponForm

# Create your views here.


def add_coupon(request):

    if request.method == 'POST':
        form = CouponForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('coupon_list')  # Redirect to your coupon list view
    
    coupon_form={
        'form':CouponForm
    }

    return render(request, 'Coupon/add_coupon.html', coupon_form)

def coupon_list(request):
    coupons = Coupon.objects.all()
    return render(request, 'Coupon/coupon_list.html', {'coupons': coupons})


class CouponDetail(View):
    template_name = 'Coupon/coupon_details.html'

    def get(self, request, coupon_id):
        coupon = Coupon.objects.get(pk=coupon_id)
        return render(request, self.template_name, {'coupon': coupon})
    
def edit_coupon(request, coupon_id):
    coupon = get_object_or_404(Coupon, pk=coupon_id)

    if request.method == 'POST':
        form = CouponForm(request.POST, instance=coupon)
        if form.is_valid():
            form.save()
            #messages.success(request, 'Coupon updated successfully.')
            return redirect('coupon_list')  # Redirect to the coupon list view
    else:
        form = CouponForm(instance=coupon)

    return render(request, 'Coupon/edit_coupon.html', {'form': form, 'coupon': coupon})