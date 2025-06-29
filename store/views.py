# store/views.py

"""Views for the store app, handling product listings, cart, and checkout."""

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.http import JsonResponse, Http404, HttpResponse
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt
from django.template.loader import render_to_string
from django.core.paginator import Paginator
from django.views.generic import View
from django.conf import settings
from django.urls import reverse
import json
import logging
import uuid
from .models import SafeProduct, StoreLocation, WishlistItem, Order, OrderItem
from .mpesa import initiate_stk_push
from .stripe import create_payment_intent

logger = logging.getLogger(__name__)

def product_list(request, category=None):
    """
    Render the product list page with filtered, sorted, and paginated products.

    Products are sorted by price in ascending order, with Cabinet category products
    appearing last (also sorted by price). Adds dimensions, weight, capacity, and
    fire class attributes with their icons to each product.

    Args:
        request: HTTP request object.
        category (str, optional): Category to filter products by. Defaults to None.

    Returns:
        HttpResponse: Rendered template with product context.
    """
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

    # Sort products: non-Cabinet first, then Cabinet, both by price ascending
    products = products.order_by('category', 'price')
    products = sorted(products, key=lambda p: (p.category == 'cabinet', p.price))

    # Add specification attributes and icons to each product with fallbacks
    for product in products:
        specs = product.specifications.all()
        product.dimensions = next((s.value for s in specs if s.name == 'Dimensions'), None)
        product.weight = next((s.value for s in specs if s.name == 'Weight'), None)
        product.capacity = next((s.value for s in specs if s.name == 'Capacity'), None)
        product.fire_class = next((s.value for s in specs if s.name == 'Fire Class'), None)
        product.dimensions_icon = next((f"icons/{s.icon}" for s in specs if s.name == 'Dimensions' and s.icon), 'icons/ruler.svg')
        product.weight_icon = next((f"icons/{s.icon}" for s in specs if s.name == 'Weight' and s.icon), 'icons/weight.svg')
        product.capacity_icon = next((f"icons/{s.icon}" for s in specs if s.name == 'Capacity' and s.icon), 'icons/water.svg')
        product.fire_class_icon = next((f"icons/{s.icon}" for s in specs if s.name == 'Fire Class' and s.icon), 'icons/fire.svg')

    # Categories for filter
    categories = valid_categories

    # Pagination
    page_obj = None
    if products:
        paginator = Paginator(products, 6)  # 6 products per page
        page_number = request.GET.get('page', 1)
        try:
            page_obj = paginator.get_page(page_number)
        except:
            logger.warning(f"Invalid page number: {page_number} for category: {category}")
            page_obj = paginator.get_page(1)
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
    """Render the product detail page for a specific product."""
    product = get_object_or_404(SafeProduct, slug=slug)
    logger.debug(f"Viewing product detail: {slug}")
    return render(request, 'store/product_detail.html', {'product': product})

@require_POST
def add_to_cart(request):
    """Add a product to the user's cart via a POST request."""
    try:
        if request.content_type == 'application/json':
            data = json.loads(request.body)
            logger.debug(f"JSON POST to add_to_cart: {data}")
        else:
            data = request.POST
            logger.debug(f"Form POST to add_to_cart: {data}")
        
        product_id = data.get('product_id')
        slug = data.get('slug')
        quantity = int(data.get('quantity', 1))
        if quantity < 1:
            quantity = 1

        if product_id:
            product = get_object_or_404(SafeProduct, id=product_id)
        elif slug:
            product = get_object_or_404(SafeProduct, slug=slug)
        else:
            raise ValueError("Product ID or slug is required")

        cart = request.session.get('cart', {})
        if product.slug in cart:
            cart[product.slug]['quantity'] += quantity
        else:
            cart[product.slug] = {'quantity': quantity, 'price': str(product.price)}
        request.session['cart'] = cart
        request.session.modified = True
        logger.debug(f"Added to cart: {product.slug}, Quantity: {quantity}, Session Cart: {cart}")
        return JsonResponse({
            'status': 'success',
            'message': f"{product.name} added to cart",
            'price': str(product.price),
            'cart_count': sum(item['quantity'] for item in cart.values()),
        })
    except ValueError as e:
        logger.warning(f"Invalid add_to_cart request: {str(e)}")
        return JsonResponse({'status': 'error', 'message': str(e)}, status=400)
    except SafeProduct.DoesNotExist:
        logger.warning(f"Product not found for ID: {product_id} or slug: {slug}")
        return JsonResponse({'status': 'error', 'message': 'Product not found'}, status=404)
    except Exception as e:
        logger.error(f"Unexpected error in add_to_cart: {str(e)}")
        return JsonResponse({'status': 'error', 'message': str(e)}, status=500)

@require_POST
def add_to_wishlist(request, slug):
    """Add or remove a product from the user's wishlist via a POST request."""
    if request.method == 'POST':
        product = get_object_or_404(SafeProduct, slug=slug)
        wishlist = request.session.get('wishlist', [])
        if product.slug not in wishlist:
            wishlist.append(product.slug)
            request.session['wishlist'] = wishlist
            request.session.modified = True
            logger.debug(f"Added to wishlist: {slug}, Wishlist: {wishlist}")
            return JsonResponse({
                'status': 'success',
                'message': f"{product.name} added to wishlist",
                'action': 'added'
            })
        else:
            wishlist.remove(product.slug)
            request.session['wishlist'] = wishlist
            request.session.modified = True
            logger.debug(f"Removed from wishlist: {slug}, Wishlist: {wishlist}")
            return JsonResponse({
                'status': 'success',
                'message': f"{product.name} removed from wishlist",
                'action': 'removed'
            })
    logger.warning(f"Invalid add_to_wishlist request for {slug}")
    return JsonResponse({'status': 'error', 'message': 'Invalid request'}, status=400)

def newsletter_signup(request):
    """Handle newsletter signup via a POST request."""
    if request.method == 'POST':
        email = request.POST.get('email')
        if email:
            messages.success(request, f"Thank you for subscribing with {email}!", extra_tags='newsletter')
            return redirect('home')
        else:
            messages.error(request, "Please enter a valid email address.", extra_tags='newsletter')
    return redirect('home')

def store_locations(request):
    """Render the store locations page."""
    locations = StoreLocation.objects.all()
    return render(request, 'store/locations.html', {'locations': locations})

def cart_view(request):
    """Render the cart page or return cart data via AJAX."""
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
        logger.debug(f"Removed invalid slugs: {invalid_slugs}")

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
    logger.debug(f"Rendering cart view: {len(cart_items)} items, Total: Ksh {total_price}")
    return render(request, 'store/cart.html', context)

@require_POST
def update_cart(request):
    """Update the user's cart based on client-side changes."""
    try:
        data = json.loads(request.body)
        client_cart = data.get('cart', {})
        server_cart = request.session.get('cart', {})

        logger.debug(f"Received update_cart request: client_cart={client_cart}, server_cart={server_cart}")

        for slug, item in list(server_cart.items()):
            if isinstance(item, dict) and 'quantity' in item and 'price' in item:
                if slug not in client_cart or client_cart.get(slug, {}).get('quantity', 0) == 0:
                    del server_cart[slug]
                    logger.debug(f"Removed item from cart: {slug}")
                elif slug in client_cart:
                    try:
                        product = SafeProduct.objects.get(slug=slug)
                        new_quantity = max(1, int(client_cart[slug].get('quantity', 1)))
                        if float(client_cart[slug].get('price', 0)) != float(product.price):
                            logger.warning(f"Price mismatch for {slug}: Client Ksh {client_cart[slug].get('price')}")
                        server_cart[slug] = {
                            'quantity': new_quantity,
                            'price': str(product.price),
                        }
                        logger.debug(f"Updated item in cart: {slug}, Quantity: {new_quantity}")
                    except SafeProduct.DoesNotExist:
                        logger.warning(f"Invalid slug in update_cart: {slug}")
                        del server_cart[slug]

        for slug, item in client_cart.items():
            if slug not in server_cart and isinstance(item, dict) and 'quantity' in item and item['quantity'] > 0:
                try:
                    product = SafeProduct.objects.get(slug=slug)
                    server_cart[slug] = {
                        'quantity': max(1, int(item['quantity'])),
                        'price': str(product.price),
                    }
                    logger.debug(f"Added new item to cart: {slug}, Quantity: {item['quantity']}")
                except SafeProduct.DoesNotExist:
                    logger.warning(f"Invalid slug in update_cart: {slug}")

        request.session['cart'] = server_cart
        request.session.modified = True
        logger.debug(f"Updated cart via update_cart: {server_cart}")
        return JsonResponse({'status': 'success'})
    except Exception as e:
        logger.error(f"Error updating cart: {str(e)}")
        return JsonResponse({'status': 'error', 'message': str(e)}, status=400)

class CheckoutView(View):
    """Handle checkout process for the user's cart."""
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
            'payment_methods': Order.PAYMENT_CHOICES,
            'stripe_public_key': settings.STRIPE_PUBLIC_KEY,
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
                shipping_address=request.POST.get('address'),
                is_paid=False,
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
            
            if order.payment_method == 'MPESA':
                formatted_phone = format_phone(request.POST.get('phone'))
                response = initiate_stk_push(formatted_phone, order.total_price, order.id)
                if response.get('ResponseCode') == '0':
                    order.checkout_request_id = response.get('CheckoutRequestID')
                    order.save()
                    return JsonResponse({
                        'status': 'success',
                        'message': 'M-Pesa payment initiated. Please complete the payment on your phone.',
                        'redirect_url': reverse('store:payment_pending', kwargs={'order_id': order.id})
                    })
                else:
                    order.delete()
                    logger.error(f"M-Pesa initiation failed for order {order.order_number}: {response}")
                    return JsonResponse({
                        'status': 'error',
                        'message': 'Failed to initiate M-Pesa payment. Please try again.'
                    }, status=400)
            
            elif order.payment_method in ['VISA', 'MASTERCARD']:
                payment_intent = create_payment_intent(order)
                if payment_intent:
                    return JsonResponse({
                        'status': 'success',
                        'client_secret': payment_intent.client_secret,
                        'order_id': order.id
                    })
                else:
                    order.delete()
                    logger.error(f"Stripe payment intent creation failed for order {order.order_number}")
                    return JsonResponse({
                        'status': 'error',
                        'message': 'Failed to initiate card payment. Please try again.'
                    }, status=400)
            
        except Exception as e:
            logger.error(f"Error processing order: {str(e)}")
            return JsonResponse({
                'status': 'error',
                'message': f"Error processing order: {str(e)}"
            }, status=400)

@csrf_exempt
def mpesa_callback(request):
    """Handle M-Pesa callback to confirm payment status."""
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            result_code = data['Body']['stkCallback']['ResultCode']
            order_id = data['Body']['stkCallback']['Metadata'][0]['Value'].split('-')[1]
            order = get_object_or_404(Order, id=order_id)
            
            if result_code == 0:
                order.is_paid = True
                order.save()
                clear_cart(request, order.session_key)
                logger.info(f"M-Pesa payment successful for order {order.order_number}")
                return HttpResponse(status=200)
            else:
                order.delete()
                logger.error(f"M-Pesa payment failed for order {order.order_number}: {data['Body']['stkCallback']['ResultDesc']}")
                return HttpResponse(status=200)
        except Exception as e:
            logger.error(f"Error in M-Pesa callback: {str(e)}")
            return HttpResponse(status=400)
    return HttpResponse(status=400)

def payment_pending(request, order_id):
    """Render the payment pending page for a specific order."""
    order = get_object_or_404(Order, id=order_id)
    return render(request, 'store/payment_pending.html', {'order': order})

def payment_success(request):
    """Render the payment success page for a completed order."""
    order_id = request.GET.get('order_id')
    order = get_object_or_404(Order, id=order_id)
    if not order.is_paid:
        order.is_paid = True
        order.save()
        clear_cart(request, order.session_key)
    return render(request, 'store/payment_success.html', {'order': order})

def payment_failure(request):
    """Render the payment failure page."""
    return render(request, 'store/payment_failure.html')

def order_confirmation(request, order_id):
    """Render the order confirmation page."""
    order = get_object_or_404(Order, id=order_id)
    return render(request, 'store/order_confirmation.html', {'order': order})

def order_detail(request, order_number):
    """Render the order detail page for a specific order."""
    if request.user.is_authenticated:
        order = get_object_or_404(Order, order_number=order_number, user=request.user)
    else:
        order = get_object_or_404(Order, order_number=order_number, session_key=request.session.session_key)
    return render(request, 'store/order_detail.html', {'order': order})

def debug_session(request):
    """Return session data for debugging."""
    return JsonResponse({
        'session_cart': request.session.get('cart', {}),
        'session_wishlist': request.session.get('wishlist', []),
        'session_key': request.session.session_key,
    })

def format_phone(phone):
    """Format phone number to +254 format for M-Pesa."""
    phone = phone.strip().replace(' ', '')
    if phone.startswith('0'):
        return f"+254{phone[1:]}"
    elif phone.startswith('+254'):
        return phone
    elif phone.startswith('254'):
        return f"+254{phone[3:]}"
    return phone

def clear_cart(request, session_key):
    """Clear the cart for the given session."""
    request.session['cart'] = {}
    request.session.modified = True
    logger.debug(f"Cart cleared for session {session_key}")
