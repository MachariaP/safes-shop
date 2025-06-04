from .models import StoreLocation


def store_data(request):
    primary_location = StoreLocation.objects.filter(is_primary=True).first()
    return {
            'primary_location' : primary_location
            }
