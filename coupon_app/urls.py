from . import views
from django.urls import path

urlpatterns = [
    path('coupon_list', views.coupon_list, name='coupon_list'),
    path('add_coupon/', views.add_coupon, name='add_coupon'),
    path('CouponDetail/<int:coupon_id>/', views.CouponDetail.as_view(), name='CouponDetail'),
    path('edit_coupon/<int:coupon_id>/', views.edit_coupon, name='edit_coupon'),
    
    
]