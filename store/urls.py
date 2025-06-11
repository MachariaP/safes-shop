from django.urls import path, re_path
from django.shortcuts import redirect
from . import views

app_name = 'store'

urlpatterns = [
    path('', views.product_list, name='product_list'),
    path('locations/', views.store_locations, name='store_locations'),
    path('product-<str:slug>/', views.product_detail, name='product_detail'),
    path('<str:category>/', views.product_list, name='category_product_list'),
    re_path(r'^store/(?P<slug>[-\w]+)/$', lambda request, slug: redirect('store:product_detail', slug=slug, permanent=True)),
    path('add-to-cart/<str:slug>/', views.add_to_cart, name='add_to_cart'),
    path('add-to-wishlist/<str:slug>/', views.add_to_wishlist, name='add_to_wishlist'),
    path('cart/', views.cart_view, name='cart'),
    path('update-cart/', views.update_cart, name='update_cart'),
    path('checkout/', views.CheckoutView.as_view(), name='checkout'),
    path('order-confirmation/<int:order_id>/', views.order_confirmation, name='order_confirmation'),
]
