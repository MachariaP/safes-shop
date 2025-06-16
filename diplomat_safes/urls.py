"""
URL configuration for diplomat_safes project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))

"""

from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from store import views
from store.views import product_list

urlpatterns = [
    path('', product_list, name='home'),  # Homepage maps to store's product_list view
    path('newsletter/signup/', views.newsletter_signup, name='newsletter_signup'),
    path('store/', include('store.urls')),  # Store app URLs
    path('', include('core.urls', namespace='core')),  # Core app URLs
    path('users/', include('users.urls')),  # Users app URLs
    path('payments/', include('payments.urls')),  # Payments app URLs
    path('referrals/', include('referrals.urls')),  # Referrals app URLs
    path('admin/', admin.site.urls),  # Admin interface
    path('accounts/', include('allauth.urls')),  # django-allauth URLs
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
