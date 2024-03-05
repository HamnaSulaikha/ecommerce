from django.urls import path
from .views import ExportOrdersToPDF
from . import views

urlpatterns = [
    path('', views.admin_login, name='admin_login'),
    path('dashboard/',views.dashboard, name='dashboard'),
    path('user_management/', views.user_management, name='user_management'),
    path('activate_user/<int:user_id>/', views.activate_user, name='activate_user'),
    path('deactivate_user/<int:user_id>/', views.deactivate_user, name='deactivate_user'), 
    path('category2/', views.category2, name='category2'),
    path('add_category/', views.add_category, name='add_category'),
    path('edit_category/<int:category_id>', views.edit_category, name='edit_category'),
    path('delete_category/<int:category_id>/', views.delete_category, name='delete_category'),
    path('admin_order_list/', views.admin_order_list, name='admin_order_list'),
    path('edit_order/<int:order_id>/', views.edit_order, name='edit_order'),
    path('export_orders_to_csv/',views.export_orders_to_csv,name='export_orders_to_csv'),
    path('export-orders-to-pdf/', ExportOrdersToPDF.as_view(), name='export_orders_to_pdf'),
]
