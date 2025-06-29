# Diplomat Safes E-commerce Platform

![Diplomat Safes Logo](static/images/logo.png)

Welcome to **Diplomat Safes**, a modern e-commerce platform offering premium security solutions for homes and businesses. Built with **Django 4.2** and **Bootstrap 5.3**, this platform provides a seamless and secure shopping experience with **M-Pesa**, **Visa**, **Mastercard** payments, and social authentication via Google and Facebook.

[Visit Live Demo](https://diplomat-safes.example.com) | [Explore Documentation](#installation)

---

## ✨ Key Features

- 🛒 **Browse & Search Safes**: Discover a wide range of safes with detailed product views and specifications.
- 🔐 **Secure Authentication**: Login, signup, and logout with Google or Facebook, enhanced with password visibility toggles.
- 💳 **Flexible Payments**: Pay securely via M-Pesa or credit/debit cards (Visa, Mastercard) using Stripe.
- 📦 **Cart & Order Management**: Add items to cart, update quantities in real-time with AJAX, and track orders.
- 📱 **Responsive Design**: Optimized for mobile, tablet, and desktop devices.
- ⚡ **Enhanced UX**: Features skeleton loading screens, accessibility-focused UI, and smooth touch interactions.

---

## 📸 Screenshots

| **Login Page** | **Cart Page** |
|----------------|---------------|
| ![Login Page](docs/screenshots/login.png) | ![Cart Page](docs/screenshots/cart.png) |
| Secure login with social auth and password toggle | Real-time cart updates with AJAX and payment options |

---

## 🛠️ Technology Stack

- **Backend**: Python 3.10, Django 4.2, PostgreSQL, django-allauth, Celery
- **Frontend**: Bootstrap 5.3, JavaScript, Font Awesome 6.4
- **Payments**: Safaricom M-Pesa API, Stripe API
- **Deployment**: Configurable for Heroku, AWS, or other platforms (see [Deployment](#deployment))

---

## 🚀 Quick Start

### Prerequisites
- Python 3.10+
- PostgreSQL 14+
- Git
- M-Pesa and Stripe API credentials
- Google and Facebook OAuth credentials

### Installation

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/MachariaP/safes-shop.git
   cd safes-shop

Set Up Virtual Environment:
bash

python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows

Install Dependencies:
bash

pip install -r requirements.txt

Configure Environment Variables:
Create a .env file in the project root:
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

Start the Development Server:
bash

python manage.py runserver

Access the app at http://127.0.0.1:8000.

 Code Snippets
Real-time Cart Updates (static/js/cart.js)
javascript

document.addEventListener('DOMContentLoaded', () => {
    const cart = {
        async updateCart() {
            try {
                const response = await fetch('/store/cart/', {
                    headers: { 'X-Requested-With': 'XMLHttpRequest' }
                });
                if (!response.ok) throw new Error('Network response was not ok');
                const data = await response.json();
                document.getElementById('cart-total').textContent = `Ksh ${data.total.toFixed(2)}`;
                document.getElementById('cart-count').textContent = data.count;
            } catch (error) {
                console.error('Cart update failed:', error);
                document.getElementById('cart-error').textContent = 'Failed to update cart. Please try again.';
            }
        }
    };
    cart.updateCart();
    document.addEventListener('cartUpdated', () => cart.updateCart());
});

M-Pesa Payment Integration (payments/views.py)
python

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import requests
from django.conf import settings

@csrf_exempt
def initiate_mpesa_payment(request):
    if request.method == 'POST':
        phone = request.POST.get('phone')
        amount = request.POST.get('amount')
        if not phone or not amount:
            return JsonResponse({'error': 'Missing phone or amount'}, status=400)
        payload = {
            "BusinessShortCode": settings.MPESA_SHORTCODE,
            "Amount": amount,
            "PartyA": phone,
            "CallBackURL": settings.MPESA_CALLBACK_URL,
            "TransactionDesc": "Diplomat Safes Purchase"
        }
        headers = {'Authorization': f'Bearer {get_mpesa_access_token()}'}
        try:
            response = requests.post(settings.MPESA_STK_PUSH_URL, json=payload, headers=headers)
            response.raise_for_status()
            return JsonResponse(response.json())
        except requests.RequestException as e:
            return JsonResponse({'error': f'Payment initiation failed: {str(e)}'}, status=500)
    return JsonResponse({'error': 'Invalid request method'}, status=400)

 Deployment
To deploy the platform (e.g., on Heroku or AWS):
Configure a production-ready database (e.g., PostgreSQL on AWS RDS).

Set DEBUG=False in .env and update ALLOWED_HOSTS with your domain.

Use a WSGI server like Gunicorn:
bash

pip install gunicorn
gunicorn diplomat_safes.wsgi

Serve static files via a CDN or server (e.g., AWS S3).

Configure environment variables in your hosting platform.

Set up a reverse proxy (e.g., Nginx) for production.

For detailed steps, see DEPLOYMENT.md (create this file if needed).
 Contributing
We welcome contributions! To get started:
Fork the repository.

Create a feature branch (git checkout -b feature/your-feature).

Commit changes (git commit -m "Add your feature").

Push to the branch (git push origin feature/your-feature).

Open a Pull Request.

Please follow our Code of Conduct (CODE_OF_CONDUCT.md) and ensure tests pass:
bash

python manage.py test

 License
This project is licensed under the MIT License. See LICENSE for details.
 Contact
Email: walburphinehas78@gmail.com (mailto:walburphinehas78@gmail.com)

GitHub: MachariaP

Website: Diplomat Safes

Diplomat Safes © 2025 - Premium Security Solutions

