import os
import django
import sys

# Add current directory to path
sys.path.append(os.getcwd())

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ngo_website.settings')
django.setup()

from django.conf import settings

def check_config():
    print("Checking SITE_CONFIG...")
    sc = settings.SITE_CONFIG
    required_sc = ['SITE_NAME', 'SITE_TAGLINE', 'SITE_DESCRIPTION', 'LOGO_PATH', 'CONTACT_EMAIL', 'CONTACT_PHONE', 'CONTACT_ADDRESS', 'SOCIAL_MEDIA']
    for key in required_sc:
        if key not in sc:
            print(f"  [ERROR] SITE_CONFIG missing key: '{key}'")
    
    print("Checking PAYMENT_CONFIG...")
    pc = settings.PAYMENT_CONFIG
    required_pc = ['UPI_VPA', 'UPI_PAYEE_NAME', 'SUPPORTED_UPI_APPS', 'MINIMUM_DONATION', 'CURRENCY', 'TRANSACTION_PREFIX']
    for key in required_pc:
        if key not in pc:
            print(f"  [ERROR] PAYMENT_CONFIG missing key: '{key}'")

check_config()
