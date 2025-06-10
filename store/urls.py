from django.urls import path, re_path
from django.shortcuts import redirect
from . import views

app_name = 'store'

urlpatterns = [
    path('', views.product_list, name='product_list'),
    path('locations/', views.store_locations, name='store_locations'),
    path('product-<str:slug>/', views.product_detail, name='product_detail'),  # Prioritize product detail
    path('<str:category>/', views.product_list, name='category_product_list'),  # Category after
    re_path(r'^store/(?P<slug>[-\w]+)/$', lambda request, slug: redirect('store:product_detail', slug=slug, permanent=True)),  # Redirect old slugs
]
