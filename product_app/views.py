from django.shortcuts import redirect, render
from .forms import VariantForm,ProductForm
from .models import Review
from store.models import Category,Product,Variant
from django.contrib import messages
from django.contrib.auth.models import User
from django.shortcuts import render, get_object_or_404

# Create your views here.

def add_product(request):
    categories = Category.objects.all()  # Fetch categories for the dropdown

    if request.method == 'POST':
        name = request.POST.get('name')
        description = request.POST.get('description')
        category_id = request.POST.get('category')
        price = request.POST.get('price')
        brand = request.POST.get('brand')
        rating = request.POST.get('rating')
        image = request.FILES.get('image')
        discount_percentage = request.POST.get('discount_percentage', None)

        try:
            product = Product.objects.create(
                name=name,
                description=description,
                category=Category.objects.get(id=category_id),
                price=price,
                brand=brand,
                rating=rating,
                image=image,
                discount_percentage=discount_percentage
            )
            return redirect('product_detail', product.id)  # Redirect to product detail page
        except Exception as e:
            
            print(e)
            return render(request, 'product/Add_product.html', {'categories': categories, 'error': 'Error creating product'})
    else:
        return render(request, 'product/Add_product.html', {'categories': categories})


def admin_product(request):
    products = Product.objects.all()  
    return render(request, 'product/admin_product.html', {'products': products})

def add_variant(request, product_id):
    product = get_object_or_404(Product, id=product_id)

    if request.method == 'POST':
        color = request.POST.get('color')
        stock = request.POST.get('stock')

        price_modifier = request.POST.get('price_modifier')
        fittings = request.POST.get('fittings')
        quality = request.POST.get('quality')
        features = request.POST.get('features')

        image = request.FILES.get('image')
        image2 = request.FILES.get('image2')
        image3 = request.FILES.get('image3')

        try:
           Variant.objects.create(
                product=product,
                color=color,
                stock=stock,
                price_modifier=price_modifier,
                fittings=fittings,
                quality=quality,
                features=features,
             
                image=image,
                image2=image2,
                image3=image3,
            )
           
           return redirect('admin_product')  # Redirect to product list
        
        except Exception as e:
            # Handle errors during variant creation
            print(e)
            return render(request, 'product/Add_variant.html', {'product': product, 'error': 'Error creating variant'})
    else:
        return render(request, 'product/Add_variant.html', {'product': product})
    
def product_detail(request, product_id):

    product = get_object_or_404(Product, id=product_id)
    variants = Variant.objects.filter(product=product)

    for variant in variants:
        variant.total_price = product.price + variant.price_modifier

    context = {
        'product': product,
        'variants': variants,
    }

    return render(request, 'product/variants.html', context)

def edit_variant(request, variant_id):
    
    variant = get_object_or_404(Variant, pk=variant_id)

    if request.method == 'POST':
        # Process form data
        form = VariantForm(request.POST, instance=variant)
        if form.is_valid():
            form.save()
            return redirect('product_detail', product_id=variant.product.id)
    else:
        form = VariantForm(instance=variant)

    context = {
        'form': form,
    }
    return render(request, 'product/edit_variant.html', context)


def edit_product(request, product_id):
    product = get_object_or_404(Product, pk=product_id)
    
    if request.method == 'POST':
        form = ProductForm(request.POST, instance=product)
        if form.is_valid():
            form.save()
            return redirect('product_detail', product_id=product.id)

    
    else:
        form = ProductForm(instance=product)

    context = {
        'form': form,
    }
    return render(request, 'product/edit_product.html', context)

def add_review(request, variant_id):
    variant = Variant.objects.get(pk=variant_id)
    print(f"Variant ID: {variant_id}")

    if request.method == 'POST':
        rating = request.POST.get('rating')
        review_text = request.POST.get('review_text')

        if not rating or not review_text:
            messages.error(request, 'Please provide a rating and review text.')
            

        review = Review.objects.create(
            user=request.user,
            variant=variant,
            rating=int(rating),
            review_text=review_text,
        )

        messages.success(request, 'Your review has been submitted successfully!')
        return redirect('home')

    return render(request, 'product/review.html', {'variant': variant})