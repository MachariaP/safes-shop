import requests
import base64
from datetime import datetime
from django.conf import settings
import logging

logger = logging.getLogger(__name__)

def get_mpesa_access_token():
    """Fetch M-Pesa OAuth access token"""
    consumer_key = settings.MPESA_CONFIG['CONSUMER_KEY']
    consumer_secret = settings.MPESA_CONFIG['CONSUMER_SECRET']
    auth_str = f"{consumer_key}:{consumer_secret}"
    encoded_auth = base64.b64encode(auth_str.encode()).decode()
    headers = {
        'Authorization': f'Basic {encoded_auth}',
    }
    url = 'https://sandbox.safaricom.co.ke/oauth/v1/generate?grant_type=client_credentials'
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        return response.json()['access_token']
    except Exception as e:
        logger.error(f"Failed to get M-Pesa access token: {str(e)}")
        return None

def generate_mpesa_password():
    """Generate M-Pesa password for STK Push"""
    shortcode = settings.MPESA_CONFIG['SHORTCODE']
    passkey = settings.MPESA_CONFIG['PASSKEY']
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    data = f"{shortcode}{passkey}{timestamp}"
    return base64.b64encode(data.encode()).decode()

def initiate_stk_push(phone, amount, order_id):
    """Initiate M-Pesa STK Push payment"""
    if settings.DEBUG:
        logger.debug(f"Mocking M-Pesa STK Push for order {order_id}")
        return {
            'ResponseCode': '0',
            'CheckoutRequestID': f'mock_checkout_request_id_{order_id}',
            'ResponseDescription': 'Success'
        }

    access_token = get_mpesa_access_token()
    if not access_token:
        return {'ResponseCode': '1', 'ResponseDescription': 'Failed to get access token'}

    headers = {
        'Authorization': f'Bearer {access_token}',
        'Content-Type': 'application/json'
    }
    payload = {
        "BusinessShortCode": settings.MPESA_CONFIG['SHORTCODE'],
        "Password": generate_mpesa_password(),
        "Timestamp": datetime.now().strftime("%Y%m%d%H%M%S"),
        "TransactionType": "CustomerPayBillOnline",
        "Amount": str(int(amount)),
        "PartyA": phone,
        "PartyB": settings.MPESA_CONFIG['SHORTCODE'],
        "PhoneNumber": phone,
        "CallBackURL": settings.MPESA_CONFIG['CALLBACK_URL'],
        "AccountReference": f"ORDER-{order_id}",
        "TransactionDesc": "Online Purchase"
    }
    
    try:
        response = requests.post(
            settings.MPESA_CONFIG['STK_PUSH_URL'],
            json=payload,
            headers=headers
        )
        response.raise_for_status()
        logger.debug(f"M-Pesa STK Push initiated for order {order_id}: {response.json()}")
        return response.json()
    except Exception as e:
        logger.error(f"Failed to initiate M-Pesa STK Push for order {order_id}: {str(e)}")
        return {'ResponseCode': '1', 'ResponseDescription': str(e)}
