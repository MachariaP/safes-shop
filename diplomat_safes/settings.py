# diplomat_safes/settings.py
import environ
import os
from pathlib import Path
import dj_database_url

BASE_DIR = Path(__file__).resolve().parent.parent

# Initialize environment
env = environ.Env()
env.read_env(BASE_DIR / '.env')

SECRET_KEY = env('SECRET_KEY')
DEBUG = env.bool('DEBUG', default=False)
ALLOWED_HOSTS = env.list('ALLOWED_HOSTS', default=['localhost', '127.0.0.1'])

# Application definition
INSTALLED_APPS = [
    #'django_admin_charts',
    'jazzmin',
    'diplomat_safes',
    'store',
    'users',
    'payments',
    'referrals',
    'core',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'allauth.socialaccount.providers.google',
    'allauth.socialaccount.providers.facebook',
    'crispy_forms',
    'crispy_bootstrap5',
    'ckeditor',
]

SITE_ID = 1

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'allauth.account.middleware.AccountMiddleware',
]

# Session settings
SESSION_ENGINE = 'django.contrib.sessions.backends.db'
SESSION_COOKIE_AGE = 1209600
SESSION_COOKIE_SECURE = False
SESSION_COOKIE_SAMESITE = 'Lax'
SESSION_SAVE_EVERY_REQUEST = True

# Logging configuration
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
        },
        'file': {
            'class': 'logging.FileHandler',
            'filename': 'debug.log',
        },
    },
    'loggers': {
        'store': {
            'handlers': ['console', 'file'],
            'level': 'DEBUG',
            'propagate': True,
        },
    },
}

ROOT_URLCONF = 'diplomat_safes.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'store.context_processors.store_data',
            ],
        },
    },
]

WSGI_APPLICATION = 'diplomat_safes.wsgi.application'

# Database
DATABASES = {
    'default': env.db(),
}



# Authentication
AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend',
    'allauth.account.auth_backends.AuthenticationBackend',
]

AUTH_USER_MODEL = 'users.CustomUser'

# Allauth settings
ACCOUNT_LOGIN_METHODS = {'email', 'username'}  # Replaces ACCOUNT_AUTHENTICATION_METHOD
ACCOUNT_SIGNUP_FIELDS = ['email*', 'password1*', 'password2*']  # Replaces ACCOUNT_EMAIL_REQUIRED, ACCOUNT_SIGNUP_PASSWORD_ENTER_TWICE, ACCOUNT_USERNAME_REQUIRED
ACCOUNT_EMAIL_VERIFICATION = 'none'
LOGIN_REDIRECT_URL = '/store/'
ACCOUNT_LOGOUT_REDIRECT_URL = '/'
ACCOUNT_SIGNUP_REDIRECT_URL = '/store/'
SOCIALACCOUNT_LOGIN_ON_GET = True

# Social providers
SOCIALACCOUNT_PROVIDERS = {
    'google': {
        'APP': {
            'client_id': env('GOOGLE_CLIENT_ID'),
            'secret': env('GOOGLE_CLIENT_SECRET'),
            'key': '',
        },
        'SCOPE': ['profile', 'email'],
        'AUTH_PARAMS': {'access_type': 'online'},
    },
    'facebook': {
        'APP': {
            'client_id': env('FACEBOOK_APP_ID'),
            'secret': env('FACEBOOK_APP_SECRET'),
            'key': '',
        },
        'METHOD': 'oauth2',
        'SCOPE': ['email', 'public_profile'],
        'VERSION': 'v20.0',
    },
}

# Crispy forms
CRISPY_ALLOWED_TEMPLATE_PACKS = 'bootstrap5'
CRISPY_TEMPLATE_PACK = 'bootstrap5'

# URLs
LOGIN_URL = '/accounts/login/'

# Static files
STATIC_URL = '/static/'
STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static')]
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATICFILES_FINDERS = [
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
]

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

CKEDITOR_CONFIGS = {
    'default': {
        'allowedContent': True,
        'toolbar': 'Full',
        'contentsCss': '/static/css/ckeditor.css',
        'autoParagraph': False,
        'basicEntities': False,
        'entities': False,
        'entities_latin': False,
        'htmlEncodeOutput': False,
        'forcePasteAsPlainText': False,
    }
}

SILENCED_SYSTEM_CHECKS = ['ckeditor.W001']

JAZZMIN_SETTINGS = {
    "site_title": "Diplomat Safes Admin",
    "site_header": "Diplomat Safes",
    "site_brand": "Diplomat Safes",
    "site_logo": "img/logo.png",
    "welcome_sign": "Welcome to Diplomat Safes Admin",
    "copyright": "Diplomat Safes Ltd",
    "search_model": [
        "store.SafeProduct",
        "users.CustomUser",
        "core.TeamMember",
        "core.Solution",
        "core.Testimonial",
        "store.StoreLocation",
        "store.Order",
    ],
    "topmenu_links": [
        {"name": "Home", "url": "admin:index", "permissions": ["auth.view_user"]},
        {"name": "View Site", "url": "/", "new_window": True},
    ],
    "usermenu_links": [
        {"name": "Support", "url": "https://example.com/support", "new_window": True},
    ],
    "show_sidebar": True,
    "navigation_expanded": True,
    "hide_apps": [],
    "hide_models": [],
    "order_with_respect_to": ["auth", "users", "store", "core"],
    "icons": {
        "users.CustomUser": "fas fa-user",
        "store.SafeProduct": "fas fa-box",
        "store.ProductSpecification": "fas fa-list",
        "store.StoreLocation": "fas fa-map-marker-alt",
        "store.WishlistItem": "fas fa-heart",
        "store.Order": "fas fa-shopping-cart",
        "store.OrderItem": "fas fa-cart-plus",
        "core.TeamMember": "fas fa-user-tie",
        "core.Solution": "fas fa-lightbulb",
        "core.Testimonial": "fas fa-quote-left",
        "core.Profile": "fas fa-user",
    },
    "default_icon_parents": "fas fa-chevron-circle-right",
    "default_icon_children": "fas fa-circle",
    "changeform_format": "horizontal_tabs",
    "show_ui_builder": True,
}


JAZZMIN_UI_TWEAKS = {
    "theme": "cyborg",  # Bootswatch theme for vivid look [][](https://djangocentral.com/making-django-admin-jazzy-with-django-jazzmin/)
    "dark_mode_theme": "darkly",
    "sidebar": "sidebar-dark-primary",
    "navbar": "navbar-dark",
    "brand_colour": "navbar-primary",
    "accent": "accent-primary",
    "sidebar_nav_compact_style": True,
    "sidebar_disable_expand": False,
    "sidebar_nav_child_indent": True,
    "sidebar_nav_flat_style": True,
    "footer_fixed": False,
}

# AWS S3 settings
AWS_ACCESS_KEY_ID = env('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = env('AWS_SECRET_ACCESS_KEY')
AWS_STORAGE_BUCKET_NAME = env('AWS_STORAGE_BUCKET_NAME')
AWS_S3_REGION_NAME = 'us-east-1'
AWS_S3_CUSTOM_DOMAIN = f'{AWS_STORAGE_BUCKET_NAME}.s3.amazonaws.com'
AWS_DEFAULT_ACL = None  # Deprecated in newer S3; use bucket policy instead
DEFAULT_FILE_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'
MEDIA_URL = f'https://{AWS_S3_CUSTOM_DOMAIN}/'

# M-Pesa configuration
MPESA_CONFIG = {
    'CONSUMER_KEY': env('MPESA_CONSUMER_KEY'),
    'CONSUMER_SECRET': env('MPESA_CONSUMER_SECRET'),
    'SHORTCODE': env('MPESA_SHORTCODE'),
    'PASSKEY': env('MPESA_PASSKEY'),
    'STK_PUSH_URL': 'https://sandbox.safaricom.co.ke/mpesa/stkpush/v1/processrequest',
    'CALLBACK_URL': 'https://yourdomain.com/store/mpesa-callback/',
}

# Stripe configuration
STRIPE_PUBLIC_KEY = env('STRIPE_PUBLIC_KEY')
STRIPE_SECRET_KEY = env('STRIPE_SECRET_KEY')
