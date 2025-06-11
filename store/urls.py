from django.urls import path
from . import views

app_name = 'store'

urlpatterns = [
    path('', views.product_list, name='product_list'),
    path('product-<str:slug>/', views.product_detail, name='product_detail'),  # Moved before category
    path('category/<str:category>/', views.product_list, name='category_product_list'),  # Added prefix
    path('add-to-cart/<str:slug>/', views.add_to_cart, name='add_to_cart'),
    path('add-to-wishlist/<str:slug>/', views.add_to_wishlist, name='add_to_wishlist'),
    path('cart/', views.cart_view, name='cart'),
    path('update-cart/', views.update_cart, name='update_cart'),
    path('checkout/', views.CheckoutView.as_view(), name='checkout'),
    path('order-confirmation/<int:order_id>/', views.order_confirmation, name='order_confirmation'),
    path('locations/', views.store_locations, name='store_locations'),
    path('newsletter-signup/', views.newsletter_signup, name='newsletter_signup'),
    path('debug-session/', views.debug_session, name='debug_session'),
]