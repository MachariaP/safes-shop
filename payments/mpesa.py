import requests
import base64
from datetime import datetime
from django.conf import settings
import json


def get_mpesa_access_token():
    consumer_key = settings.MPESA_CONFIG['CONSUMER_KEY']
    consumer_secret = settings.MPESA_CONFIG['CONSUMER_SECRET']
    api_url = "https://sandbox.safaricom.co.ke/oauth/v1/generate?grant_type=client_credentials"

    response = requests.get(
            api_url,
            auth=( consumer_key, consumer_secret),
            headers={'Content-Type': 'application/json'}
            )

    if response.status_code == 200:
        return response.json().get('access_token')
    return None

def initiate_stk_push(phone_number, amount, account_reference, callback_url):
    access_token = get_mpesa_access_token()
    if not access_token:
        return None

    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    passkey = settings.MPESA_CONFIG['PASSKEY']
    business_shortcode = settings.MPESA_CONFIG['SHORTCODE']

    password = base64.b64encode(
            f"{business_shortcode}{passkey}{timestamp}".encode()
            ).decode()

    payload = {
            "BusinessShortCode": business_shortcode,
            "Password": password,
            "Timestamp": timestamp,
            "TransactionType": "CustomerPayBillOnline",
            "Amount": amount,
            "PartyA": phone_number,
            "PartyB": business_shortcode,
            "PhoneNumber": phone_number,
            "CallBackURL": callback_url,
            "AccountReference": account_reference,
            "TransactionDesc": "Diplomat Safes Purchase"
            }

    headers = {
            "Authorization": f"Bearer {access_token}",
            "Content-Type": "application/json"
            }

    response = requests.post(
            "https://sandbox.safaricom.co.ke/mpesa/stkpush/v1/processrequest",
            json=payload,
            headers=headers
            )

    return response.json()
