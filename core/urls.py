from django.urls import path
from .views import AboutUsView

app_name = 'core'

urlpatterns = [
    path('about-us/', AboutUsView.as_view(), name='about_us'),
]
