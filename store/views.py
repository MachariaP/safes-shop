from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.template.loader import render_to_string
from django.core.paginator import Paginator
from django.views.generic import View
import json
from .models import SafeProduct, StoreLocation, CartItem, WishlistItem, Order, OrderItem

def product_list(request, category=None):
    if request.path == '/':
        return render(request, 'home.html')

    products = SafeProduct.objects.all()
    if category:
        products = products.filter(category__iexact=category)

    # Handle sorting
    sort = request.GET.get('sort', 'name')
    if sort == 'price':
        products = products.order_by('price')
    elif sort == '-price':
        products = products.order_by('-price')
    elif sort == '-name':
        products = products.order_by('-name')
    else:
        products = products.order_by('name')

    # Categories for filter
    categories = SafeProduct.objects.values('category').distinct()

    # Pagination
    paginator = Paginator(products, 8)  # 8 products per page
    page_number = request.GET.get('page', 1)
    page_obj = paginator.get_page(page_number)

    # Handle AJAX requests
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        html = render_to_string('store/partials/product_card.html', {
            'products': page_obj.object_list,
        }, request=request)
        return JsonResponse({
            'html': html,
            'products': list(page_obj.object_list.values('id')),
        })

    context = {
        'products': page_obj.object_list,
        'page_obj': page_obj,
        'category': category,
        'categories': [{'name': cat['category']} for cat in categories],
    }
    return render(request, 'store/product_list.html', context)

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
        request.session.modified = True
        return JsonResponse({
            'status': 'success',
            'message': f"{product.name} added to cart",
            'price': str(product.price),
        })
    return JsonResponse({'status': 'error', 'message': 'Invalid request'})

def add_to_wishlist(request, slug):
    if request.method == 'POST':
        product = get_object_or_404(SafeProduct, slug=slug)
        wishlist = request.session.get('wishlist', [])
        if product.slug not in wishlist:
            wishlist.append(product.slug)
            request.session['wishlist'] = wishlist
            request.session.modified = True
            return JsonResponse({
                'status': 'success',
                'message': f"{product.name} added to wishlist",
                'action': 'added'
            })
        else:
            wishlist.remove(product.slug)
            request.session['wishlist'] = wishlist
            request.session.modified = True
            return JsonResponse({
                'status': 'success',
                'message': f"{product.name} removed from wishlist",
                'action': 'removed'
            })
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
    cart_items = []
    total_price = 0
    cart_count = 0
    invalid_slugs = []

    for slug, item in list(cart.items()):
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
            cart_count += item['quantity']  # Use quantity for accurate count
        except SafeProduct.DoesNotExist:
            invalid_slugs.append(slug)

    # Clean up invalid cart items
    if invalid_slugs:
        for slug in invalid_slugs:
            del cart[slug]
        request.session['cart'] = cart
        request.session.modified = True

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

class CheckoutView(View):
    def get(self, request):
        cart = request.session.get('cart', {})
        cart_items = []
        total_price = 0
        
        for slug, item in cart.items():
            try:
                product = SafeProduct.objects.get(slug=slug)
                item_total = float(item['price']) * item['quantity']
                cart_items.append({
                    'product': product,
                    'quantity': item['quantity'],
                    'price': float(item['price']),
                    'total': item_total,
                })
                total_price += item_total
            except SafeProduct.DoesNotExist:
                continue
        
        context = {
            'cart_items': cart_items,
            'total_price': total_price,
            'payment_methods': Order.PAYMENT_CHOICES
        }
        return render(request, 'store/checkout.html', context)
    
    def post(self, request):
        cart = request.session.get('cart', {})
        if not cart:
            messages.error(request, "Your cart is empty.")
            return redirect('store:cart')
        
        # Create order
        try:
            order = Order.objects.create(
                session_key=request.session.session_key,
                total_price=request.POST.get('total_price'),
                payment_method=request.POST.get('payment_method'),
                contact_email=request.POST.get('email'),
                contact_phone=request.POST.get('phone'),
                shipping_address=request.POST.get('address')
            )
            
            # Create order items
            for slug, item in cart.items():
                try:
                    product = SafeProduct.objects.get(slug=slug)
                    OrderItem.objects.create(
                        order=order,
                        product=product,
                        quantity=item['quantity'],
                        price=item['price']
                    )
                except SafeProduct.DoesNotExist:
                    continue
            
            # Clear cart
            request.session['cart'] = {}
            request.session.modified = True
            
            messages.success(request, "Order placed successfully!")
            return redirect('store:order_confirmation', order_id=order.id)
        except Exception as e:
            messages.error(request, f"Error processing order: {str(e)}")
            return redirect('store:checkout')

def order_confirmation(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    return render(request, 'store/order_confirmation.html', {'order': order})
