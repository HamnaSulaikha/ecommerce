from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.registerpage, name='register'),
    path('',views.loginpage,name='login'),
    path('otp_verify/', views.otp_verify, name='otp_verify'),
    path('logout/',views.logoutuser,name='logout'),
    path('user_profile/', views.user_profile, name='user_profile'),
    path('add_address/', views.add_address, name='add_address'),
    path('change_password/', views.change_password, name='change_password'),
    path('category/',views.category, name = 'category'),
    path('product_details/<int:variant_id>/', views.product_details, name='product_details'),
    path('store/<int:category_id>/',views.store, name = 'store'),
    path('add_to_cart/', views.add_to_cart, name='add_to_cart'),
    path('update-payment-status/', views.update_payment_status, name='update_payment_status'),
    
    path('decrease_quantity/<int:cart_item_id>/', views.decrease_quantity, name='decrease_quantity'),
    path('increase_quantity/<int:cart_item_id>/',views.increase_quantity, name='increase_quantity'),
    path('remove_from_cart/<int:cart_item_id>/', views.remove_from_cart, name='remove_from_cart'),
]