from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.http import require_POST
import json
from .models import SafeProduct, StoreLocation, CartItem, WishlistItem

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

def add_to_cart(request, slug):
    if request.method == 'POST':
        product = get_object_or_404(SafeProduct, slug=slug)
        quantity = int(request.POST.get('quantity', 1))
        cart = request.session.get('cart', {})
        cart_item = {'quantity': quantity, 'price': str(product.price)}
        cart[product.slug] = cart_item
        request.session['cart'] = cart
        request.session.modified = True   # Ensure session is saved
        return JsonResponse({'status': 'success', 'message': f"{product.name} added to cart"})
    return JsonResponse({'status': 'error', 'message': 'Invalid request'})

def add_to_wishlist(request, slug):
    if request.method == 'POST':
        product = get_object_or_404(SafeProduct, slug=slug)
        wishlist = request.session.get('wishlist', [])
        if product.slug not in wishlist:
            wishlist.append(product.slug)
            request.session['wishlist'] = wishlist
            return JsonResponse({'status': 'success', 'message': f"{product.name} added to wishlist", 'action': 'added'})
        else:
            wishlist.remove(product.slug)
            request.session['wishlist'] = wishlist
            return JsonResponse({'status': 'success', 'message': f"{product.name} removed from wishlist", 'action': 'removed'})
    return JsonResponse({'status': 'error', 'message': 'Invalid request'})

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

def cart_view(request):
    cart = request.session.get('cart', {})
    print("Session cart:", cart)  # Debug output
    cart_items = []
    total_price = 0
    cart_count = 0

    for slug, item in cart.items():
        try:
            product = SafeProduct.objects.get(slug=slug)
            item_total = float(item['price']) * item['quantity']
            cart_items.append({
                'product': product,
                'quantity': item['quantity'],
                'price': float(item['price']),
                'total': item_total,
                'image': product.image.url if product.image else 'https://via.placeholder.com/80',
            })
            total_price += item_total
            cart_count += 1
        except SafeProduct.DoesNotExist:
            print(f"Product with slug {slug} not found in database")  # Debug
            continue

    context = {
        'cart_items': cart_items,
        'total_price': total_price,
        'cart_count': cart_count,
    }
    return render(request, 'store/cart.html', context)

@require_POST
def update_cart(request):
    try:
        data = json.loads(request.body)
        cart = data.get('cart', {})
        request.session['cart'] = cart
        request.session.modified = True
        return JsonResponse({'status': 'success'})
    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)}, status=400)
