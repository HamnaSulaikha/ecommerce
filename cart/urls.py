from . import views
from django.urls import path
from .views import view_cart,remove_from_cart

urlpatterns = [

    path('cart/', view_cart, name='view_cart'),
    
    path('remove_from_cart/<int:cart_item_id>/',remove_from_cart, name='remove_from_cart'),

]