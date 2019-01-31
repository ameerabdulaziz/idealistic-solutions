from django.urls import path
from . import views

app_name = 'cart'

urlpatterns = [
    path('', views.CartItemListView.as_view(), name='cart-detail'),
    # path('add/<int:product_id>/', views.CartUpdateView.as_view(), name='cart-update'),
    path('add/<int:product_id>/', views.add_to_cart, name='cart-update'),
    path('checkout/', views.checkout, name='cart-checkout'),
    path('payment/', views.payment, name='cart-payment'),

    path('ajax/delete_cart_item/', views.cart_delete_ajax, name='delete-cart-item'),
    path('ajax/decrease_quantity_cart_item/', views.cart_quantity_decrease_ajax, name='decrease-quantity-cart-item'),
    path('ajax/increase_quantity_cart_item/', views.cart_quantity_increase_ajax, name='increase-quantity-cart-item'),
]
