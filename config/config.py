"""
Central configuration file for NGO website
Manages all environment-specific settings for easy deployment
"""

import os
import socket

# Detect environment based on hostname
hostname = socket.gethostname().lower()
IS_LOCALHOST = 'localhost' in hostname or '127.0.0.1' in hostname or hostname.startswith('desktop-') or hostname.startswith('laptop-')

# Database Configuration
if IS_LOCALHOST:
    import pathlib
    DATABASE_CONFIG = {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': str(pathlib.Path(__file__).resolve().parent.parent / 'db.sqlite3'),
    }
else:
    # cPanel production settings - prioritizing environment variables
    DATABASE_CONFIG = {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': os.environ.get('DB_NAME', 'cpanel_ngo_db'),
        'USER': os.environ.get('DB_USER', 'cpanel_user'),
        'PASSWORD': os.environ.get('DB_PASSWORD', 'cpanel_pass'),
        'HOST': os.environ.get('DB_HOST', 'localhost'),
        'PORT': os.environ.get('DB_PORT', '3306'),
        'OPTIONS': {
            'init_command': "SET sql_mode='STRICT_TRANS_TABLES'",
            'charset': 'utf8mb4',
        }
    }

# Site Configuration
SITE_CONFIG = {
    'SITE_NAME': 'Shree Brijwasi Jatav Samaj Sewa Samiti',
    'SITE_TAGLINE': 'Journey of Empowerment and Impact',
    'SITE_DESCRIPTION': 'A dedicated NGO working towards social empowerment and community service',
    'LOGO_PATH': 'images/logo.png',
    'LOGO_PRIMARY_COLOR': '#2563eb',      # Blue
    'LOGO_SECONDARY_COLOR': '#7c3aed',    # Purple
    'LOGO_BACKGROUND_COLOR': '#f8fafc',   # Light gray
    'CONTACT_EMAIL': 'info@brijwasisamaj.org',  # Update when email is created
    'CONTACT_PHONE': '+91 9630145866',
    'CONTACT_ADDRESS': 'BHOPAL, MADHYA PRADESH',
    'SOCIAL_MEDIA': {
        'facebook': 'https://facebook.com/brijwasisamaj',
        'twitter': 'https://twitter.com/brijwasisamaj',
        'instagram': 'https://instagram.com/brijwasisamaj',
        'youtube': 'https://youtube.com/@brijwasisamaj',
    }
}

# Payment Configuration
PAYMENT_CONFIG = {
    'UPI_VPA': os.environ.get('UPI_VPA', 'yourupi@paytm'),  # Update when UPI ID is created
    'UPI_PAYEE_NAME': os.environ.get('UPI_PAYEE_NAME', 'Shree Brijwasi Jatav Samaj Sewa Samiti'),
    'SUPPORTED_UPI_APPS': ['googlepay', 'phonepe', 'paytm', 'bhim', 'other'],
    'MINIMUM_DONATION': 100,
    'CURRENCY': 'INR',
    'TRANSACTION_PREFIX': 'SBJS',
}

# Email Configuration
if IS_LOCALHOST:
    EMAIL_CONFIG = {
        'EMAIL_BACKEND': 'django.core.mail.backends.console.EmailBackend',  # Print to console
        'EMAIL_HOST': 'smtp.gmail.com',
        'EMAIL_PORT': 587,
        'EMAIL_USE_TLS': True,
        'EMAIL_HOST_USER': 'your-email@gmail.com',
        'EMAIL_HOST_PASSWORD': 'your-app-password',
        'DEFAULT_FROM_EMAIL': 'Shree Brijwasi Jatav Samaj Sewa Samiti <noreply@brijwasisamaj.org>',
    }
else:
    EMAIL_CONFIG = {
        'EMAIL_BACKEND': 'django.core.mail.backends.smtp.EmailBackend',
        'EMAIL_HOST': os.environ.get('EMAIL_HOST', 'mail.yourdomain.com'),
        'EMAIL_PORT': int(os.environ.get('EMAIL_PORT', 587)),
        'EMAIL_USE_TLS': os.environ.get('EMAIL_USE_TLS', 'True') == 'True',
        'EMAIL_HOST_USER': os.environ.get('EMAIL_HOST_USER', 'noreply@yourdomain.com'),
        'EMAIL_HOST_PASSWORD': os.environ.get('EMAIL_HOST_PASSWORD', 'your-email-password'),
        'DEFAULT_FROM_EMAIL': os.environ.get('DEFAULT_FROM_EMAIL', 'Shree Brijwasi Jatav Samaj Sewa Samiti <noreply@yourdomain.com>'),
    }

# Media Configuration
MEDIA_CONFIG = {
    'UPLOAD_PATHS': {
        'team_photos': 'team_photos/',
        'work_projects': 'work_projects/',
        'project_gallery': 'project_gallery/',
        'media_gallery': 'media_gallery/',
    },
    'ALLOWED_IMAGE_TYPES': ['jpg', 'jpeg', 'png', 'webp', 'gif'],
    'ALLOWED_VIDEO_TYPES': ['mp4', 'webm'],
    'MAX_IMAGE_SIZE': 5,  # MB
    'MAX_VIDEO_SIZE': 50,  # MB
    'IMAGE_COMPRESSION_QUALITY': 85,
}

# Slider Configuration
SLIDER_CONFIG = {
    'SLIDER_IMAGES': [
        'images/slider/slide1.jpg',
        'images/slider/slide2.jpg',
        'images/slider/slide3.jpg',
    ],
    'SLIDER_INTERVAL': 5000,  # milliseconds
    'SLIDER_TRANSITION': 'fade',
    'SLIDER_AUTOPLAY': True,
}

# Environment-specific settings
DEBUG = IS_LOCALHOST

if IS_LOCALHOST:
    ALLOWED_HOSTS = ['localhost', '127.0.0.1']
    STATIC_ROOT = None  # Not needed for development
else:
    ALLOWED_HOSTS = ['shreebrijwasijatavsamajsevasamiti.com', 'www.shreebrijwasijatavsamajsevasamiti.com']  # Update with actual domain
    STATIC_ROOT = '/home/username/public_html/static/'  # Update with actual path
