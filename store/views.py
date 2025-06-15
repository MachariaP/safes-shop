from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.http import JsonResponse, Http404
from django.views.decorators.http import require_POST
from django.template.loader import render_to_string
from django.core.paginator import Paginator
from django.views.generic import View
import json
import logging
import uuid
from .models import SafeProduct, StoreLocation, CartItem, WishlistItem, Order, OrderItem

# Set up logging
logger = logging.getLogger(__name__)

def product_list(request, category=None):
    if request.path == '/':
        return render(request, 'home.html')

    products = SafeProduct.objects.all()
    valid_categories = SafeProduct.objects.values('category').distinct().values_list('category', flat=True)

    if category:
        if category.lower() not in [cat.lower() for cat in valid_categories]:
            logger.warning(f"Invalid category: {category}")
            raise Http404(f"Category '{category}' not found")
        products = products.filter(category__iexact=category)
        logger.debug(f"Filtering products by category: {category}")

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
    categories = valid_categories

    # Pagination
    page_obj = None
    if products.exists():
        paginator = Paginator(products, 8)  # 8 products per page
        page_number = request.GET.get('page', 1)
        try:
            page_obj = paginator.get_page(page_number)
        except:
            logger.warning(f"Invalid page number: {page_number} for category: {category}")
            page_obj = paginator.get_page(1)  # Fallback to page 1
    else:
        logger.debug(f"No products found for category: {category}")

    # Handle AJAX requests
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        html = render_to_string('store/partials/product_card.html', {
            'products': page_obj.object_list if page_obj else [],
        }, request=request)
        return JsonResponse({
            'html': html,
            'products': list(page_obj.object_list.values('id')) if page_obj else [],
        })

    context = {
        'products': page_obj.object_list if page_obj else [],
        'page_obj': page_obj,
        'category': category,
        'categories': [{'name': cat} for cat in categories],
    }
    logger.debug(f"Rendering product list: {len(context['products'])} products, Category: {category}")
    return render(request, 'store/product_list.html', context)

def product_detail(request, slug):
    product = get_object_or_404(SafeProduct, slug=slug)
    logger.debug(f"Viewing product detail: {slug}")
    return render(request, 'store/product_detail.html', {'product': product})

def add_to_cart(request, slug):
    if request.method == 'POST':
        product = get_object_or_404(SafeProduct, slug=slug)
        quantity = int(request.POST.get('quantity', 1))
        if quantity < 1:
            quantity = 1
        cart = request.session.get('cart', {})
        if slug in cart:
            cart[slug]['quantity'] += quantity
        else:
            cart[slug] = {'quantity': quantity, 'price': str(product.price)}
        request.session['cart'] = cart
        request.session.modified = True
        logger.debug(f"Added to cart: {slug}, Quantity: {quantity}, Session Cart: {cart}, Session Key: {request.session.session_key}")
        return JsonResponse({
            'status': 'success',
            'message': f"{product.name} added to cart",
            'price': str(product.price),
        })
    logger.warning(f"Invalid add_to_cart request for {slug}")
    return JsonResponse({'status': 'error', 'message': 'Invalid request'}, status=400)

def add_to_wishlist(request, slug):
    if request.method == 'POST':
        product = get_object_or_404(SafeProduct, slug=slug)
        wishlist = request.session.get('wishlist', [])
        if product.slug not in wishlist:
            wishlist.append(product.slug)
            request.session['wishlist'] = wishlist
            request.session.modified = True
            logger.debug(f"Added to wishlist: {slug}, Wishlist: {wishlist}, Session Key: {request.session.session_key}")
            return JsonResponse({
                'status': 'success',
                'message': f"{product.name} added to wishlist",
                'action': 'added'
            })
        else:
            wishlist.remove(product.slug)
            request.session['wishlist'] = wishlist
            request.session.modified = True
            logger.debug(f"Removed from wishlist: {slug}, Wishlist: {wishlist}, Session Key: {request.session.session_key}")
            return JsonResponse({
                'status': 'success',
                'message': f"{product.name} removed from wishlist",
                'action': 'removed'
            })
    logger.warning(f"Invalid add_to_wishlist request for {slug}")
    return JsonResponse({'status': 'error', 'message': 'Invalid request'}, status=400)

def newsletter_signup(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        if email:
            messages.success(request, f"Thank you for subscribing with {email}!", extra_tags='newsletter')
            return redirect('home')
        else:
            messages.error(request, "Please enter a valid email address.", extra_tags='newsletter')
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

    logger.debug(f"Fetching cart: {cart}, Session Key: {request.session.session_key}")

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
            cart_count += item['quantity']
        except SafeProduct.DoesNotExist:
            invalid_slugs.append(slug)

    if invalid_slugs:
        for slug in invalid_slugs:
            del cart[slug]
        request.session['cart'] = cart
        request.session.modified = True
        logger.debug(f"Removed invalid slugs: {invalid_slugs}, Session Key: {request.session.session_key}")

    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return JsonResponse({
            'status': 'success',
            'cart_items': [{
                'product': {'slug': item['product'].slug, 'name': item['product'].name},
                'quantity': item['quantity'],
                'price': item['price'],
                'total': item['total'],
                'image': item['image'],
            } for item in cart_items],
            'total_price': total_price,
            'cart_count': cart_count,
        })

    context = {
        'cart_items': cart_items,
        'total_price': total_price,
        'cart_count': cart_count,
    }
    logger.debug(f"Rendering cart view: {len(cart_items)} items, Total: Ksh {total_price}, Session Key: {request.session.session_key}")
    return render(request, 'store/cart.html', context)

@require_POST
def update_cart(request):
    try:
        data = json.loads(request.body)
        client_cart = data.get('cart', {})
        server_cart = request.session.get('cart', {})

        for slug, item in client_cart.items():
            if isinstance(item, dict) and 'quantity' in item and 'price' in item:
                try:
                    product = SafeProduct.objects.get(slug=slug)
                    if float(item['price']) != float(product.price):
                        logger.warning(f"Price mismatch for {slug}: Client Ksh {item['price']}, Server Ksh {product.price}")
                    server_cart[slug] = {
                        'quantity': max(1, int(item['quantity'])),
                        'price': str(product.price),  # Use server price
                    }
                except SafeProduct.DoesNotExist:
                    logger.warning(f"Invalid slug in update_cart: {slug}")
                    continue

        # Remove items not in client cart
        server_cart = {slug: server_cart[slug] for slug in client_cart if slug in server_cart}

        request.session['cart'] = server_cart
        request.session.modified = True
        logger.debug(f"Updated cart via update_cart: {server_cart}, Session Key: {request.session.session_key}")
        return JsonResponse({'status': 'success'})
    except Exception as e:
        logger.error(f"Error updating cart: {str(e)}, Session Key: {request.session.session_key}")
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
        
        try:
            order = Order.objects.create(
                user=request.user if request.user.is_authenticated else None,
                session_key=request.session.session_key,
                order_number=f"ORD-{uuid.uuid4().hex[:8].upper()}",
                total_price=float(request.POST.get('total_price')),
                payment_method=request.POST.get('payment_method'),
                contact_email=request.POST.get('email'),
                contact_phone=request.POST.get('phone'),
                shipping_address=request.POST.get('address')
            )
            
            for slug, item in cart.items():
                try:
                    product = SafeProduct.objects.get(slug=slug)
                    OrderItem.objects.create(
                        order=order,
                        product=product,
                        quantity=item['quantity'],
                        price=float(item['price'])
                    )
                except SafeProduct.DoesNotExist:
                    continue
            
            request.session['cart'] = {}
            request.session.modified = True
            logger.debug(f"Order #{order.order_number} created, cart cleared, Session Key: {request.session.session_key}")
            messages.success(request, "Order placed successfully!")
            return redirect('store:order_confirmation', order_id=order.id)
        except Exception as e:
            logger.error(f"Error processing order: {str(e)}, Session Key: {request.session.session_key}")
            messages.error(request, f"Error processing order: {str(e)}")
            return redirect('store:checkout')

def order_confirmation(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    return render(request, 'store/order_confirmation.html', {'order': order})

def order_detail(request, order_number):
    if request.user.is_authenticated:
        order = get_object_or_404(Order, order_number=order_number, user=request.user)
    else:
        order = get_object_or_404(Order, order_number=order_number, session_key=request.session.session_key)
    return render(request, 'store/order_detail.html', {'order': order})

def debug_session(request):
    return JsonResponse({
        'session_cart': request.session.get('cart', {}),
        'session_wishlist': request.session.get('wishlist', []),
        'session_key': request.session.session_key,
    })
