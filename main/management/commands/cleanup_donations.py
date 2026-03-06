"""
Management command to clean up expired/stale pending donations
"""
from django.core.management.base import BaseCommand
from main.models import Donation
from django.utils import timezone
from datetime import timedelta

class Command(BaseCommand):
    help = 'Mark pending donations older than 7 days as failed/expired'

    def handle(self, *args, **kwargs):
        expiry_limit = timezone.now() - timedelta(days=7)
        
        stale_donations = Donation.objects.filter(
            payment_status='pending',
            created_at__lt=expiry_limit
        )
        
        count = stale_donations.count()
        
        for donation in stale_donations:
            donation.payment_status = 'failed'
            donation.notes += f"\nAuto-marked as failed due to inactivity on {timezone.now().date()}"
            donation.save()
            
        self.stdout.write(self.style.SUCCESS(f'Successfully cleaned up {count} stale donations.'))
