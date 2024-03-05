from django.contrib import messages
from django.http import FileResponse
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import redirect, render
from django.contrib.auth.models import User
from django.views import View
from django.contrib.auth import authenticate,login,logout
from store.models import *
from orders.models import Order
from .forms import OrderForm
from store.models import UserProfile,Category
from django.contrib.auth.decorators import user_passes_test
from django.shortcuts import render, get_object_or_404
from django.db.models import Count,F,Sum
from django.db.models.functions import ExtractMonth
import csv
from reportlab.pdfgen import canvas
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle
from reportlab.lib.pagesizes import letter

# Create your views here.
def admin_login(request):
    if request.user.is_authenticated and request.user.is_superuser :
            return redirect('dashboard')
    else:
        if request.method == "POST":
            username = request.POST.get('username')
            password = request.POST.get('password')

            user = authenticate(request, username= username, password= password)

            if user is not None:
                login(request, user)
                return redirect('dashboard')
            else:
                messages.error(request, 'Username or Password is incorrect')

        context = {}

        return render(request, 'customadmin/login.html', context)

def admin_logout(request):
    logout(request)
    return redirect('login')


def dashboard(request):

    data = Order.objects.annotate(month=ExtractMonth('order_date')).values('month').annotate(order_count=Count('id'))
    data_amount = Order.objects.annotate(month=ExtractMonth('order_date')).values('month').annotate(order_amount=Sum('total_price'))

    month_labels_amount = [f'Month {entry["month"]}' for entry in data_amount]
    monthly_amount = [entry['order_amount'] for entry in data_amount]
    

    month_labels = [f'Month {entry["month"]}' for entry in data]
    monthly_values = [entry['order_count'] for entry in data]


    
    order_counts_by_status = Order.objects.annotate(
        status=F('delivery_status'),).values('status').annotate(count=Count('pk'))

    context = {
        'order_counts_by_status': order_counts_by_status,
        'month_labels' : month_labels,
        'monthly_values' : monthly_values,
        'month_labels_amount': month_labels_amount,
        'monthly_amount': monthly_amount,
       

    }
    return render(request,'customadmin/dashboard.html', context)
   

def user_management(request):

    dict_user = {
         'userdetails':UserProfile.objects.all(),
         'user':User.objects.all()
    }

    return render(request,'customadmin/admin_user.html',dict_user)

def activate_user(request, user_id):
    user = get_object_or_404(User, pk=user_id)
    user.is_active = True
    user.save()
    messages.success(request, f'User {user.username} has been activated.')
    return redirect('dashboard')  

def deactivate_user(request, user_id):
    user = get_object_or_404(User, pk=user_id)
    user.is_active = False
    user.save()
    messages.success(request, f'User {user.username} has been deactivated.')
    return redirect('dashboard')

def category2(request):
    
    dict_category = {
        'catgry':Category.objects.all()
    }

    return render(request,'customadmin/category2.html',dict_category)

def add_category(request):

    if request.method == 'POST':
        name = request.POST.get('name')
        description = request.POST.get('description')
        image = request.FILES.get('image')

        try:
            category = Category.objects.create(
                name = name,
                description=description,
                image=image,
            )
            return redirect('category2')
        
        except Exception as e:
            print(e)
            return redirect('category2', {'error': 'Error creating product'})

    return render(request,'customadmin/add_category.html')

def edit_category(request, category_id):
    category2 = get_object_or_404(Category, pk=category_id)

    if request.method == 'POST':
        name = request.POST.get('name')
        description = request.POST.get('description')
        image = request.FILES.get('image')

        try:
            # Update the existing object
            category2.name = name
            category2.description = description

            if image:
                category2.image = image

            category2.save()

            return redirect('category2')
        
        except Exception as e:
            print(e)
            return redirect('category2', {'error': 'Error updating category'})

    return render(request, 'customadmin/edit_category.html', {'category2': category2})

def delete_category(request, category_id):
    category = get_object_or_404(Category, pk=category_id)

    if request.method == 'POST':
        category.delete()
        return redirect('category2')

    return render(request, 'customadmin/delete_category.html', {'category2': category2})


def admin_order_list(request):
    orders = Order.objects.all()
    delivery_status_choices = Order._meta.get_field('delivery_status').choices
    payment_status_choices = Order._meta.get_field('payment_status').choices
    context = {
        'orders': orders,
        'delivery_status_choices': delivery_status_choices,
        'payment_status_choices': payment_status_choices,
    }
    return render(request, 'customadmin/order_list.html', context)

def edit_order(request, order_id):
    order = get_object_or_404(Order, pk=order_id)
    if request.method == 'POST':
        form = OrderForm(request.POST, instance=order)  
        if form.is_valid():
            form.save()
            
            return redirect('admin_order_list')  
    else:
        form = OrderForm(instance=order)  # Pre-fill form for editing
    return render(request, 'customadmin/edit_order.html', {'form': form})

def export_orders_to_csv(request):

    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="orders.csv"'

    # Create a CSV writer
    writer = csv.writer(response)

    # Write header row
    writer.writerow(['Order ID', 'User', 'Total Price', 'Order Date', 'Payment Status', 'Delivery Status', 'Payment Type'])

    # Write data rows
    orders = Order.objects.all()
    for order in orders:
        writer.writerow([order.id, order.user.username, order.total_price, order.order_date, order.payment_status, order.delivery_status, order.payment_type])

    return response

class ExportOrdersToPDF(View):

    def get(self, request, *args, **kwargs):
        # Create a response object
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename="orders.pdf"'

        # Create a PDF document
        pdf_buffer = SimpleDocTemplate(response, pagesize=letter)

        # Table data
        table_data = [['Order ID', 'User', 'Total Price', 'Order Date', 'Payment Status', 'Delivery Status', 'Payment Type']]

        # Fetch orders from the database
        orders = Order.objects.all()

        # Add order data to the table
        for order in orders:
            order_data = [order.id, order.user.username, order.total_price, order.order_date, order.payment_status, order.delivery_status, order.payment_type]
            table_data.append(order_data)

        # Create a table and set styles
        order_table = Table(table_data)
        order_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ]))

        # Build PDF document
        pdf_buffer.build([order_table])

        return response

