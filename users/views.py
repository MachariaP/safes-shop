from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib import messages
from .forms import CustomUserCreationForm
from referrals.models import Referral
from referrals.utils import award_referral_points

# Create your views here.
def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()

            # Process referral if code exists
            referral_code = form.cleaned_data.get('referral_code')
            if referral_code:
                try:
                    referrer = CustomUser.objects.grt(referral_code=referral_code)
                    Referral.objects.create(referrer=referrer, referee=user)
                except CustomUser.DoesNotExist:
                    pass

            login(request, user)
            messages.success(request, 'Registration successful!')
            return redirect('home')
    else:
        form = CustomUserCreationForm()

    return render(request, 'users/register.html', {'form': form})
