from django.shortcuts import render, get_object_or_404
from .models import SafeProduct, StoreLocation

# Create your views here.
def product_list(request):
    products = SafeProduct.objects.all()
    return render(request, 'store/product_list.html', {'products': products})

def product_detail(request, slug):
    product = get_object_or_404(SafeProduct, slug=slug)
    return render(request, 'store/product_detail.html', {'products': products})

def store_locations(request):
    locations = StoreLocation.objects.all()
    return render(request, 'store/locations.html', {'locations': locations})
