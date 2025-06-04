from django.cof import settings
from .models import Referral
from users.models import CustomUser

def award_referral_points(user):
    # Check if user was referred
    try:
        referral = Referral.objects.get(referee=user, points_awarded=False)
        referral.points_awarded = True
        referral.save()

        # Award points (100 points = 1% discount)
        referral.referrer.referral_points += 100
        referral.referrer.save()
    except Referral.DoesNotExist:
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
