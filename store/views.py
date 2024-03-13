from django.http import HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404, render, redirect
from decimal import Decimal
from product_app.models import Review
from django.db.models import Q
from orders.models import Order
from cart.models import UserCart
from .forms import CreateUserForm
import random
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import Address, Category, Product, UserProfile,Variant
from django.contrib.auth.models import User
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from .helper import MessageHandler
from django.views.decorators.csrf import csrf_exempt

# Create your views here.

def registerpage(request):
    if request.user.is_authenticated:
        return redirect('category')
    else:
        form = CreateUserForm()
        if request.method == "POST":
            form = CreateUserForm(request.POST)

            if User.objects.filter(username__iexact=request.POST['username']).exists():
                messages.error(request, "User already exists")
                return redirect('register')
            
            if form.is_valid():
                user = form.save()

                profile = UserProfile.objects.create(
                    user = user,
                    phone=form.cleaned_data['phone'],
                    age=form.cleaned_data['age'],
                )

                user_name = form.cleaned_data.get('username')
                messages.success(request, f'Account was created for {user_name}')
                return redirect('login')

        else:
            form = CreateUserForm()

        context = {'form':form}
        return render(request, 'user/register.html', context)

def loginpage(request):
    if request.user.is_authenticated:
        return redirect('category')
    else:
        if request.method == "POST":
            username = request.POST.get('username')
            password = request.POST.get('password')

            user = authenticate(request, username= username, password= password)
            otp=random.randint(1000,9999)
            
            if user is not None:
                
                login(request, user)
                
                return redirect('category')
            
            else:
                
                messages.info(request,'User name or password not matching')
                
                
    context = {}
    return render(request,'user/login.html',context)
    
def otp_verify(request):
    if request.method == "POST":
        # Perform OTP verification
        profile = UserProfile.objects.get(otp=request.POST['otp'])

        
        if profile.otp == request.POST['otp']:
            user = profile.user
            login(request, user)
 
            return redirect('category')
        return HttpResponse("10 minutes passed")

    return render(request, "user/login_otp.html")

def logoutuser(request):
    logout(request)
    return redirect('login')

def user_profile(request):

    try:
        userprofile = request.user.profile  # Retrieve the current user's profile

        if request.method == "POST":
            phone = request.POST.get('phone')
            email = request.POST.get('email')
            age = request.POST.get('age')

            userprofile.phone = phone
            userprofile.email = email
            userprofile.age = age
            userprofile.save()  # Save the updated profile

            return redirect('user_profile')
        
    except UserProfile.DoesNotExist:
        
        pass # will create new userProfile for that user

    if request.method == "POST" and request.POST.get('action') == 'add_address':
        street = request.POST.get('street')
        city = request.POST.get('city')
        state = request.POST.get('state')
        zip_code = request.POST.get('zip_code')

        address = Address.objects.create(
            street=street, city=city, state=state, zip_code=zip_code, user=request.user
        )
        return redirect('user_profile')  # Redirect to refresh the page
    
    

    return render(request, 'user/user_profile.html')

def add_address(request):

    if request.method == "POST":
        street = request.POST.get('street')
        city = request.POST.get('city')
        state = request.POST.get('state')
        zip_code = request.POST.get('pin')

        address = Address.objects.create(
            street=street, city=city, state=state, zip_code=zip_code, user=request.user
        )
        return redirect('user_profile')  # Redirect to the profile page

    return redirect('user_profile')


def change_password(request):
   

    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        print(form.is_valid())  # Add this line

        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)

            messages.success(request, 'Password changed successfully!')
            return redirect('user_profile')  # Redirect to profile page
        else:
            messages.error(request, 'Invalid password change.')
    else:  # Handle GET requests
        form = PasswordChangeForm(request.user)

    return render(request, 'user/change_password.html', {'form': form})

@login_required(login_url='login')
def category(request):
    
    dict_cat = {
        'category':Category.objects.all(),
        'variants':Variant.objects.all()
    }
    
    return render(request, 'store/category.html', dict_cat)


def store(request,  category_id):
    variants = Variant.objects.filter(product__category=category_id).all()
    
    return render(request, 'store\store.html', {'variants': variants})

def product_details(request, variant_id):
    variant = get_object_or_404(Variant, pk=variant_id)
    reviews = Review.objects.filter(variant=variant)
    product = variant.product
    variants = product.variant_set.all()
    return render(request, 'product_details.html', {'variant': variant, 'variants': variants, 'selected_variant': variant, 'reviews': reviews})

def add_to_cart(request,):
    if request.method == 'POST':
        prod_id = int(request.POST.get('product_id'))
        product_check = Variant.objects.get(id=prod_id)
        
        if(product_check):
            if(UserCart.objects.filter(user=request.user.id,product=prod_id)):
                return JsonResponse({'status':"Product Already in Cart"})
            else:
                prod_qty = int(request.POST.get('product_qty'))
                prod_name = request.POST.get('product_name')

                if product_check.stock >= prod_qty:
                    UserCart.objects.create(user=request.user,product_id=prod_id,title=prod_name,quantity=prod_qty)
                    return JsonResponse({'status':"Product added to cart"})
                else:
                    return JsonResponse({'status':"Only"+str(product_check.stock)+"available"})
        else:
            return JsonResponse({'status':"No such product found"})
    

    return redirect('view_cart')  # Redirect to the product details page    


@csrf_exempt
def update_payment_status(request):
    print("update payment function started")
    if request.method == 'POST':
        order_id = request.POST.get('order_id')

        print(order_id)

        order = Order.objects.get(id=order_id)
        order.payment_status = 'Paid'
        order.save()

        return JsonResponse({'status': 'success', 'payment_status': order.payment_status})

    return JsonResponse({'status': 'error'})




def decrease_quantity(request, cart_item_id):
    cart_item = get_object_or_404(UserCart, id=cart_item_id)
    cart_item.quantity = max(0, cart_item.quantity - 1)
    cart_item.save()

    if cart_item.quantity == 0:
        cart_item.delete()

    cart = UserCart.objects.filter(user=request.user)
    total = sum(Decimal(item.sub_total) for item in cart)

    data = {
        'status': 'success',
        'message': 'Quantity decreased.',
        'subtotal': cart_item.sub_total,
        'total': total
    }
    return JsonResponse(data)

def increase_quantity(request, cart_item_id):
    cart_item = get_object_or_404(UserCart, id=cart_item_id)
    cart_item.quantity += 1
    cart_item.save()

    user = request.user

    cart= UserCart.objects.filter(Q(user=user) & Q(is_checkout_done=False))



    cart = UserCart.objects.filter(user=request.user)
    cart_total = sum(Decimal(item.sub_total) for item in cart)
    print(cart_item.sub_total)
    print(cart_total)

    data = {
        'status': 'success',
        'message': 'Quantity increased.',
        'subtotal': cart_item.sub_total,
        'total': cart_total  
    }
    return JsonResponse(data)

def remove_from_cart(request, cart_item_id):
    cart_item = get_object_or_404(UserCart, id=cart_item_id)
    cart_item.delete()

    cart = UserCart.objects.get(user=request.user)
    
    data = {
        'status': 'success',
        'message': 'Item removed from cart.',
        
    }
    return JsonResponse(data)


