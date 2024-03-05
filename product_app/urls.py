from . import views
from django.urls import path

urlpatterns = [
    path('add_product/', views.add_product, name='add_product'),
    path('admin_product/', views.admin_product, name='admin_product'),
    path('add_variant/<int:product_id>/', views.add_variant, name='add_variant'),
    path('product_detail/<int:product_id>/', views.product_detail, name='product_detail'),
    path('edit_variant/<int:variant_id>/', views.edit_variant, name='edit_variant'),
    path('edit_product/<int:product_id>/', views.edit_product, name='edit_product'),
    path('add_review/<int:variant_id>/', views.add_review, name='add_review'),


] 
