from django.urls import path
from .views import (
    product_list,
    product_detail,
    add_to_cart,
    add_to_wishlist,
    cart_view,
    update_cart,
    CheckoutView,
    order_detail,
    order_confirmation,
    store_locations,
    newsletter_signup,
    debug_session,
    mpesa_callback,
    payment_pending,
    payment_success,
    payment_failure,
)

app_name = 'store'

urlpatterns = [
    path('', product_list, name='product_list'),
    path('product-<str:slug>/', product_detail, name='product_detail'),
    path('category/<str:category>/', product_list, name='category_product_list'),
    path('add-to-cart/', add_to_cart, name='add_to_cart'),  # Updated to remove <str:slug>
    path('add-to-wishlist/<str:slug>/', add_to_wishlist, name='add_to_wishlist'),
    path('cart/', cart_view, name='cart'),
    path('update-cart/', update_cart, name='update_cart'),
    path('checkout/', CheckoutView.as_view(), name='checkout'),
    path('order/<str:order_number>/', order_detail, name='order_detail'),
    path('order-confirmation/<int:order_id>/', order_confirmation, name='order_confirmation'),
    path('locations/', store_locations, name='store_locations'),
    path('newsletter-signup/', newsletter_signup, name='newsletter_signup'),
    path('debug-session/', debug_session, name='debug_session'),
    path('mpesa-callback/', mpesa_callback, name='mpesa_callback'),
    path('payment-pending/<int:order_id>/', payment_pending, name='payment_pending'),
    path('payment-success/', payment_success, name='payment_success'),
    path('payment-failure/', payment_failure, name='payment_failure'),
]
