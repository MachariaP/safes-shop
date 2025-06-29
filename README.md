# 🌟 Diplomat Safes E-commerce Platform

![Diplomat Safes Logo](static/images/logo.png)

**Welcome to Diplomat Safes**, your premier destination for top-tier security solutions! This modern e-commerce platform, built with **Django 4.2** and **Bootstrap 5.3**, offers a secure and seamless shopping experience with **M-Pesa**, **Visa**, and **Mastercard** payments, plus social login via **Google** and **Facebook**.

👉 **[Stay Tuned for Live Demo](#live-demo)** | **[Get Started](#installation)**

---

## 🎉 Why Choose Diplomat Safes?

- 🛒 **Extensive Product Range**: Browse and search a wide selection of safes with detailed specs.
- 🔐 **Secure & Easy Access**: Login or sign up with social accounts, featuring password toggles.
- 💳 **Flexible Payments**: Pay securely with M-Pesa or credit cards via Stripe.
- 📦 **Smart Shopping**: Real-time cart updates and order tracking.
- 📱 **Mobile-Friendly**: Perfectly optimized for all devices.
- ✨ **Modern Design**: Enjoy skeleton loading, accessibility, and smooth touch interactions.

---

## 📷 Screenshots

| **Login Page**                          | **Cart Page**                          |
|-----------------------------------------|----------------------------------------|
| ![Login Page](docs/screenshots/login.png) | ![Cart Page](docs/screenshots/cart.png) |
| *Secure login with social auth & toggle* | *AJAX-powered cart with payment options* |

---

## 🛠️ Tech Stack

- **Backend**: Python 3.10, Django 4.2, PostgreSQL, django-allauth, Celery
- **Frontend**: Bootstrap 5.3, JavaScript, Font Awesome 6.4
- **Payments**: Safaricom M-Pesa API, Stripe API

---

## 🚀 Live Demo

The full platform is under deployment. Check back soon for the live demo at [Diplomat Safes](https://diplomat-safes.herokuapp.com) (coming soon)!

---

## 🛠️ Installation

### Prerequisites
- Python 3.10+
- PostgreSQL 14+
- Git
- API credentials (M-Pesa, Stripe, Google, Facebook)

### Steps
1. **Clone the Repo**:
   ```bash
   git clone https://github.com/MachariaP/safes-shop.git
   cd safes-shop

Set Up Environment:
bash

python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows
pip install -r requirements.txt

Configure:
Create .env with your API keys (see Environment (#environment)).

Run Migrations:
bash

python manage.py migrate

Start Server:
bash

python manage.py runserver

Visit http://127.0.0.1:8000.

Environment
ini

SECRET_KEY=your_secret_key
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1
DB_NAME=diplomat_safes
DB_USER=your_db_user
DB_PASSWORD=your_db_password
MPESA_CONSUMER_KEY=your_mpesa_key
...

 Code Highlights
Cart Update (static/js/cart.js)
javascript

document.addEventListener('DOMContentLoaded', () => {
    const cart = {
        async updateCart() {
            try {
                const response = await fetch('/store/cart/', { headers: { 'X-Requested-With': 'XMLHttpRequest' } });
                const data = await response.json();
                document.getElementById('cart-total').textContent = `Ksh ${data.total.toFixed(2)}`;
                document.getElementById('cart-count').textContent = data.count;
            } catch (error) {
                console.error('Error:', error);
            }
        }
    };
    cart.updateCart();
    document.addEventListener('cartUpdated', cart.updateCart);
});

M-Pesa Payment (payments/views.py)
python

@csrf_exempt
def initiate_mpesa_payment(request):
    if request.method == 'POST':
        phone = request.POST.get('phone')
        amount = request.POST.get('amount')
        payload = {
            "BusinessShortCode": settings.MPESA_SHORTCODE,
            "Amount": amount,
            "PartyA": phone,
            "CallBackURL": settings.MPESA_CALLBACK_URL
        }
        headers = {'Authorization': f'Bearer {get_mpesa_access_token()}'}
        response = requests.post(settings.MPESA_STK_PUSH_URL, json=payload, headers=headers)
        return JsonResponse(response.json())
    return JsonResponse({'error': 'Invalid request'}, status=400)

 Contribute
Fork this repo.

Create a branch (git checkout -b feature/new-feature).

Commit changes (git commit -m "Add new feature").

Push and open a PR.

 License
MIT License (LICENSE)
 Contact
Email: walburphinehas78@gmail.com (mailto:walburphinehas78@gmail.com)

GitHub: MachariaP

© 2025 Diplomat Safes - Premium Security Solutions

