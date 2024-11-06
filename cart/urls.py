from django.urls import path

from . import views

urlpatterns=[
    path('cartdetails/',views.cart_details,name='cartdetails'),
    path('add/<int:product_id>/',views.add_cart,name='addcart'),
    path('cart_decrement/<int:product_id>/',views.min_cart,name='cart_decrement'),
    path('remove/<int:product_id>/',views.cart_delete,name='remove'),
    path('checkout/', views.checkout_view, name='checkout'),
    path('order-confirmation/<int:order_id>/', views.order_confirmation, name='order_confirmation'),
]