from django.urls import path
from .views import AboutUsView, ContactView, SolutionsView, AccountView

app_name = 'core'

urlpatterns = [
    path('', AboutUsView.as_view(), name='home'),  # Added for homepage
    path('about-us/', AboutUsView.as_view(), name='about_us'),
    path('contact/', ContactView.as_view(), name='contact'),
    path('solutions/', SolutionsView.as_view(), name='solutions'),
    path('account/', AccountView.as_view(), name='account'),
]
