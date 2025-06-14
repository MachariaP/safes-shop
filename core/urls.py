from django.urls import path
from .views import AboutUsView, ContactView, SolutionsView

app_name = 'core'

urlpatterns = [
    path('about-us/', AboutUsView.as_view(), name='about_us'),
    path('contact/', ContactView.as_view(), name='contact'),
    path('solutions/', SolutionsView.as_view(), name='solutions'),
]
