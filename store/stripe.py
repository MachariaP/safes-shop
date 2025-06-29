import stripe
from django.conf import settings
import logging

logger = logging.getLogger(__name__)

stripe.api_key = settings.STRIPE_SECRET_KEY

def create_payment_intent(order):
    """Create Stripe PaymentIntent for card payment"""
    if settings.DEBUG:
        logger.debug(f"Mocking Stripe PaymentIntent for order {order.order_number}")
        return {'client_secret': f'mock_client_secret_{order.id}'}

    try:
        intent = stripe.PaymentIntent.create(
            amount=int(order.total_price * 100),  # Convert to cents
            currency='kes',
            payment_method_types=['card'],
            metadata={
                'order_id': order.id,
                'order_number': order.order_number
            },
            receipt_email=order.contact_email
        )
        logger.debug(f"Stripe PaymentIntent created for order {order.order_number}: {intent.id}")
        return intent
    except stripe.error.StripeError as e:
        logger.error(f"Failed to create Stripe PaymentIntent for order {order.order_number}: {str(e)}")
        return None
