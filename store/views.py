from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.utils.safestring import mark_safe
from .models import SafeProduct, StoreLocation

# Create your views here.
def product_list(request, category=None):
    if request.path == '/':
        return render(request, 'home.html')
    products = SafeProduct.objects.all()
    if category:
        products = products.filter(category__iexact=category)
    return render(request, 'store/product_list.html', {'products': products, 'category': category})

def product_detail(request, slug):
    product = get_object_or_404(SafeProduct, slug=slug)
    return render(request, 'store/product_detail.html', {'product': product})

def newsletter_signup(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        if email:
            messages.success(request, f"Thank you for subscribing with {email}!")
            return redirect('home')
        else:
            messages.error(request, "Please enter a valid email address.")
    return redirect('home')

def store_locations(request):
    locations = StoreLocation.objects.all()
    return render(request, 'store/locations.html', {'locations': locations})
