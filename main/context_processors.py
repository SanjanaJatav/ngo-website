"""
Custom context processor to make site configuration available in all templates
"""

from django.conf import settings
from .models import SiteSettings
from config.config import PAYMENT_CONFIG as DEFAULT_PAYMENT_CONFIG
from config.config import SITE_CONFIG as DEFAULT_SITE_CONFIG
from config.config import SLIDER_CONFIG as DEFAULT_SLIDER_CONFIG


def site_context(request):
    """
    Make site configuration and settings available in all templates
    """
    site_settings = SiteSettings.get_settings()

    # Start with default dictionaries, then override with any admin values
    dynamic_site = getattr(settings, 'SITE_CONFIG', DEFAULT_SITE_CONFIG).copy()
    # Contact overrides
    if site_settings.contact_email:
        dynamic_site['CONTACT_EMAIL'] = site_settings.contact_email
    if site_settings.contact_phone:
        dynamic_site['CONTACT_PHONE'] = site_settings.contact_phone
    if site_settings.contact_address:
        dynamic_site['CONTACT_ADDRESS'] = site_settings.contact_address
    # Social media merge
    social = dynamic_site.setdefault('SOCIAL_MEDIA', {})
    # ensure all expected keys exist to avoid template errors
    for key in ['facebook', 'twitter', 'instagram', 'youtube']:
        social.setdefault(key, '')
    if isinstance(site_settings.social_media_links, dict):
        social.update(site_settings.social_media_links)

    # Payment config possibly overridden
    dynamic_payment = getattr(settings, 'PAYMENT_CONFIG', DEFAULT_PAYMENT_CONFIG).copy()
    if site_settings.donation_upi_vpa:
        dynamic_payment['UPI_VPA'] = site_settings.donation_upi_vpa

    return {
        'SITE_CONFIG': dynamic_site,
        'PAYMENT_CONFIG': dynamic_payment,
        'SLIDER_CONFIG': getattr(settings, 'SLIDER_CONFIG', DEFAULT_SLIDER_CONFIG),
        'site_settings': site_settings,
        'current_path': request.path,
    }
