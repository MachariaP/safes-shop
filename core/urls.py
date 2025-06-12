from django.urls import path
from .views import AboutUsView, ContactView

app_name = 'core'

urlpatterns = [
    path('about-us/', AboutUsView.as_view(), name='about_us'),
    path('contact/', ContactView.as_view(), name='contact'),
]
