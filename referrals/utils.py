from django.conf import settings
from .models import Referral
from users.models import CustomUser

def award_referral_points(user, referral_code):
    if referral_code:
        try:
            referrer = CustomUser.objects.get(referral_code=referral_code)
            Referral.objects.create(referrer=referrer, referee=user)
            referrer.referral_points += 10  # Example points
            referrer.save()
            user.referral_points += 5  # Example points for referee
            user.save()
        except CustomUser.DoesNotExist:
            pass

def apply_referral_discount(user, amount):
    points = user.referral_points
    max_discount = min(points // 100, 20) # Max 20% discount

    if max_discount > 0:
        discount = (amount * max_discount) / 100
        user.referral_points -= max_discount * 100
        user.save()
        return discount

    return 0
