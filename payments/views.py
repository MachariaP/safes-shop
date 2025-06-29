from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.urls import reverse
from .models import MpesaTransaction
from .mpesa import initiate_stk_push
import uuid

# Create your views here.
@login_required
def initiate_payment(request):
    if request.method == 'POST':
        phone_number = request.POST.get('phone_number')
        amount = request.POST.get('amount')

        # Create transaction record
        transaction = MpesaTransaction.objects.create(
                user=request.user,
                amount=amount,
                phone_number=phone_number,
                checkout_request_id=str(uuid.uuid4())
        )
        
        # Initiate STK push
        callback_url = request.build_absolute_uri(
                reverse('payment_callback')
                )

        response = initiate_stk_push(
                phone_number,
                amount,
                f"SAFE-{transaction.id}",
                callback_url
                )

        if response and response.get('ResponseCode') == '0':
            transaction.merchant_request_id = response.get('MerchantRequestID')
            transaction.save()
            return render(request, 'payments/payment_pending.html', {
                'transaction': transaction
                })

        # Handle error
        transaction.status = 'failed'
        transaction.save()
        return render(request, 'payments/payment_error.html', {
            'error' : response.get('errorMessage') if response else 'Payment initiation failed'
            })

        return render(request, 'payments/payment_form.html')

def payment_callback(request):
    # Handle M-pesa callback
    data = json.loads(request.body)

    # Process callback data and update transaction
    # This would include verification and updating transaction status

    return HttpResponse(status=200)
