from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.decorators import login_required
from store.models import Variant
from decimal import Decimal
from django.db.models import Q
from .models import UserCart
from django.http import JsonResponse
from django.views.decorators.http import require_POST

# Create your views here.

def view_cart(request):
    user = request.user

     # Retrieve the user's cart
    cart = UserCart.objects.filter(Q(user=user) & Q(is_checkout_done=False))

    cart_total = sum(Decimal(item.sub_total) for item in cart)

    context =  {'cart_items': cart,'total':cart_total}

    return render(request, 'cart/cart.html', context)


@require_POST
def remove_from_cart(request, cart_item_id):

    cart_item = get_object_or_404(UserCart, id=cart_item_id)
    cart_item.delete()

    cart = UserCart.objects.get(user=request.user)
    cart.update_total_price()

    return redirect('view_cart')