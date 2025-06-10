from django.contrib.auth.decorators import login_required
from django.shortcuts import render

# Create your views here.
@login_required
def referral_dashboard(request):
    referrals = request.user.referrals_made.filter(points_awarded=True)
    return render(request, 'referrals/dashboard.html', {
        'referrals': referrals,
        'points': request.user.referral_points
        })
