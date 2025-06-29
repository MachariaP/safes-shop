# Diplomat Safes E-commerce Platform

A modern e-commerce platform for Diplomat Safes, offering premium security solutions. Built with Django and Bootstrap 5, it provides secure shopping with M-Pesa, Visa, Mastercard payments, and social authentication.

## Features

- 🛒 Browse and search safes with detailed views
- 🔐 Secure login, signup, and logout with Google/Facebook
- 💳 Pay via M-Pesa or credit cards
- 📦 Manage cart and track orders
- 📱 Responsive design for all devices
- ✨ Professional UI with password toggles and loading states

## Screenshots

![Login Page](docs/screenshots/login.png)
*Login page with social auth and password toggle*

![Cart Page](docs/screenshots/cart.png)
*Cart page with AJAX updates and payment options*

## Technology Stack

- **Backend**: Python 3.10, Django 4.2, PostgreSQL, django-allauth, Celery
- **Frontend**: Bootstrap 5.3, JavaScript, Font Awesome 6.4
- **Payments**: Safaricom M-Pesa API, Stripe API

## Code Snippets

### Cart Functionality (`static/js/cart.js`)

```javascript
document.addEventListener('DOMContentLoaded', () => {
    const cart = {
        async updateCart() {
            try {
                const response = await fetch('/store/cart/', { headers: { 'X-Requested-With': 'XMLHttpRequest' } });
                const data = await response.json();
                document.getElementById('cart-total').textContent = `Ksh ${data.total.toFixed(2)}`;
                document.getElementById('cart-count').textContent = data.count;
            } catch (error) {
                console.error('Cart update failed:', error);
            }
        }
    };
    cart.updateCart();
    document.addEventListener('cartUpdated', () => cart.updateCart());
});

M-Pesa Payment (payments/views.py)
python

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import requests

@csrf_exempt
def initiate_mpesa_payment(request):
    if request.method == 'POST':
        phone = request.POST.get('phone')
        amount = request.POST.get('amount')
        payload = {
            "BusinessShortCode": settings.MPESA_SHORTCODE,
            "Amount": amount,
            "PartyA": phone,
            "CallBackURL": settings.MPESA_CALLBACK_URL,
            "TransactionDesc": "Diplomat Safes Purchase"
        }
        headers = {'Authorization': f'Bearer {get_mpesa_access_token()}'}
        response = requests.post(settings.MPESA_STK_PUSH_URL, json=payload, headers=headers)
        return JsonResponse(response.json())
    return JsonResponse({'error': 'Invalid request'}, status=400)

Installation
Prerequisites
Python 3.10+

PostgreSQL 14+

Git

Setup Steps
Set Up Virtual Environment:
bash

python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows

Install Dependencies:
bash

pip install -r requirements.txt

Configure Environment:
Create .env in the project root:
ini

SECRET_KEY=your_secret_key_here
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1
DB_NAME=diplomat_safes
DB_USER=your_db_user
DB_PASSWORD=your_db_password
DB_HOST=localhost
DB_PORT=5432
MPESA_CONSUMER_KEY=your_mpesa_key
MPESA_CONSUMER_SECRET=your_mpesa_secret
MPESA_SHORTCODE=your_shortcode
MPESA_STK_PUSH_URL=https://sandbox.safaricom.co.ke/mpesa/stkpush/v1/processrequest
MPESA_CALLBACK_URL=https://your-callback-url
STRIPE_PUBLIC_KEY=your_stripe_public_key
STRIPE_SECRET_KEY=your_stripe_secret_key
GOOGLE_CLIENT_ID=your_google_client_id
GOOGLE_CLIENT_SECRET=your_google_client_secret
FACEBOOK_APP_ID=your_facebook_app_id
FACEBOOK_SECRET=your_facebook_secret

Run Migrations:
bash

python manage.py migrate

Create Superuser:
bash

python manage.py createsuperuser

Collect Static Files:
bash

python manage.py collectstatic

Start Server:
bash

python manage.py runserver

Access at http://127.0.0.1:8000.

License
MIT License. See LICENSE for details.
Contact
Email: walburphinehas78@gmail.com (mailto:walburphinehas78@gmail.com)
Diplomat Safes © 2025 - Premium Security Solutions


