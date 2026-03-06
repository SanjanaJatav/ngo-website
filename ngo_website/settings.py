"""
Django settings for ngo_website project.
Imports configuration from config.config module for easy deployment
"""

from pathlib import Path
import os
import sys

# Import central configuration
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from config.config import (
    DATABASE_CONFIG, SITE_CONFIG, PAYMENT_CONFIG, 
    EMAIL_CONFIG, MEDIA_CONFIG, SLIDER_CONFIG,
    DEBUG, ALLOWED_HOSTS, STATIC_ROOT as CONFIG_STATIC_ROOT
)

# Build paths inside the project
BASE_DIR = Path(__file__).resolve().parent.parent

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ.get('SECRET_KEY', 'django-insecure-development-key-replace-in-prod')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = DEBUG

ALLOWED_HOSTS = ALLOWED_HOSTS

# Application definition
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'main',  # Main application
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'ngo_website.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'main.context_processors.site_context',  # Custom context processor
            ],
        },
    },
]

WSGI_APPLICATION = 'ngo_website.wsgi.application'

# Database configuration from config.py
DATABASES = {
    'default': DATABASE_CONFIG
}

# Password validation
AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# Internationalization
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'Asia/Kolkata'
USE_I18N = True
USE_TZ = True

# Static files (CSS, JavaScript, Images)
STATIC_URL = '/static/'
STATICFILES_DIRS = [BASE_DIR / 'static']

if CONFIG_STATIC_ROOT:
    STATIC_ROOT = CONFIG_STATIC_ROOT

# Media files
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

# Default primary key field type
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Email configuration from config.py
EMAIL_BACKEND = EMAIL_CONFIG['EMAIL_BACKEND']
EMAIL_HOST = EMAIL_CONFIG['EMAIL_HOST']
EMAIL_PORT = EMAIL_CONFIG['EMAIL_PORT']
EMAIL_USE_TLS = EMAIL_CONFIG['EMAIL_USE_TLS']
EMAIL_HOST_USER = EMAIL_CONFIG['EMAIL_HOST_USER']
EMAIL_HOST_PASSWORD = EMAIL_CONFIG['EMAIL_HOST_PASSWORD']
DEFAULT_FROM_EMAIL = EMAIL_CONFIG['DEFAULT_FROM_EMAIL']

# Make configs available globally
SITE_CONFIG = SITE_CONFIG
PAYMENT_CONFIG = PAYMENT_CONFIG
MEDIA_CONFIG = MEDIA_CONFIG
SLIDER_CONFIG = SLIDER_CONFIG

# Security settings for production
if not DEBUG:
    SECURE_SSL_REDIRECT = True
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True
    SECURE_BROWSER_XSS_FILTER = True
    SECURE_CONTENT_TYPE_NOSNIFF = True
    X_FRAME_OPTIONS = 'DENY'
