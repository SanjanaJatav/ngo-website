"""
Database models for NGO website
Implements all data structures as per PRD specifications
"""

from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify
from django.core.mail import send_mail
from django.conf import settings
from django.utils import timezone
import uuid


class Donation(models.Model):
    """Track all donation transactions and donor information"""
    
    PAYMENT_APP_CHOICES = [
        ('googlepay', 'Google Pay'),
        ('phonepe', 'PhonePe'),
        ('paytm', 'Paytm'),
        ('bhim', 'BHIM'),
        ('other', 'Other UPI App'),
    ]
    
    PAYMENT_STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('completed', 'Completed'),
        ('failed', 'Failed'),
        ('refunded', 'Refunded'),
    ]
    
    donor_name = models.CharField(max_length=200)
    donor_email = models.EmailField()
    donor_phone = models.CharField(max_length=15, blank=True, null=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    upi_transaction_id = models.CharField(max_length=100, unique=True, blank=True, null=True)
    payment_app = models.CharField(max_length=20, choices=PAYMENT_APP_CHOICES)
    payment_status = models.CharField(max_length=20, choices=PAYMENT_STATUS_CHOICES, default='pending')
    transaction_reference = models.CharField(max_length=50, unique=True, blank=True)
    donation_purpose = models.TextField(blank=True)
    is_anonymous = models.BooleanField(default=False)
    receipt_sent = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    completed_at = models.DateTimeField(null=True, blank=True)
    notes = models.TextField(blank=True)
    
    class Meta:
        ordering = ['-created_at']
        verbose_name = "Donation"
        verbose_name_plural = "Donations"
        indexes = [
            models.Index(fields=['donor_email']),
            models.Index(fields=['transaction_reference']),
            models.Index(fields=['payment_status']),
            models.Index(fields=['created_at']),
        ]
    
    def save(self, *args, **kwargs):
        if not self.transaction_reference:
            self.transaction_reference = self.generate_transaction_reference()
        super().save(*args, **kwargs)
    
    def generate_transaction_reference(self):
        """Generate unique transaction reference"""
        prefix = settings.PAYMENT_CONFIG['TRANSACTION_PREFIX']
        timestamp = timezone.now().strftime('%Y%m%d%H%M%S')
        unique_id = str(uuid.uuid4().hex[:6]).upper()
        return f"{prefix}{timestamp}{unique_id}"
    
    def send_receipt_email(self):
        """Send thank you email with professional HTML receipt"""
        from .models import SiteSettings
        site_settings = SiteSettings.get_settings()
        site_name = site_settings.homepage_hero_title or settings.SITE_CONFIG.get('SITE_NAME')
        contact_address = site_settings.contact_address or settings.SITE_CONFIG.get('CONTACT_ADDRESS')
        subject = f"Donation Receipt - {site_name}"
        date_str = self.completed_at.strftime('%d %B %Y') if self.completed_at else timezone.now().strftime('%d %B %Y')
        
        html_message = f"""
        <div style="font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; max-width: 600px; margin: 0 auto; border: 1px solid #e2e8f0; border-radius: 12px; overflow: hidden;">
            <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); padding: 30px; text-align: center; color: white;">
                <h1 style="margin: 0; font-size: 24px;">Donation Receipt</h1>
                <p style="margin: 10px 0 0; opacity: 0.9;">Thank you for your generosity</p>
            </div>
            <div style="padding: 30px; color: #1e293b; line-height: 1.6;">
                <p>Dear <strong>{self.donor_name}</strong>,</p>
                <p>We are deeply grateful for your generous contribution. Your support enables us to continue our mission of social empowerment and community service.</p>
                
                <div style="background: #f8fafc; border-radius: 8px; padding: 20px; margin: 25px 0;">
                    <h3 style="margin-top: 0; color: #7c3aed; font-size: 18px; border-bottom: 2px solid #e2e8f0; padding-bottom: 10px;">Transaction Summary</h3>
                    <table style="width: 100%; border-collapse: collapse;">
                        <tr>
                            <td style="padding: 8px 0; color: #64748b;">Reference:</td>
                            <td style="padding: 8px 0; text-align: right; font-weight: 600;">{self.transaction_reference}</td>
                        </tr>
                        <tr>
                            <td style="padding: 8px 0; color: #64748b;">Amount:</td>
                            <td style="padding: 8px 0; text-align: right; color: #2563eb; font-weight: 700; font-size: 20px;">₹{self.amount}</td>
                        </tr>
                        <tr>
                            <td style="padding: 8px 0; color: #64748b;">Date:</td>
                            <td style="padding: 8px 0; text-align: right;">{date_str}</td>
                        </tr>
                        <tr>
                            <td style="padding: 8px 0; color: #64748b;">Payment Method:</td>
                            <td style="padding: 8px 0; text-align: right;">{self.get_payment_app_display()}</td>
                        </tr>
                    </table>
                </div>
                
                <p>This receipt confirms that your donation has been successfully verified and added to our impact funds.</p>
                
                <p style="margin-top: 30px;">Warm regards,<br><strong>The Team at {site_name}</strong></p>
            </div>
            <div style="background: #f1f5f9; padding: 20px; text-align: center; font-size: 12px; color: #94a3b8;">
                <p style="margin: 0;">This is an automated receipt. Please do not reply to this email.</p>
                <p style="margin: 5px 0 0;">{site_name} | {contact_address}</p>
            </div>
        </div>
        """
        
        plain_message = f"Dear {self.donor_name}, Thank you for your donation of ₹{self.amount}. Reference: {self.transaction_reference}."
        
        send_mail(
            subject, 
            plain_message, 
            settings.DEFAULT_FROM_EMAIL, 
            [self.donor_email],
            html_message=html_message
        )
        self.receipt_sent = True
        self.save()
    
    def mark_completed(self, upi_transaction_id):
        """Update status when payment verified"""
        self.payment_status = 'completed'
        self.upi_transaction_id = upi_transaction_id
        self.completed_at = timezone.now()
        self.save()
        self.send_receipt_email()
    
    def __str__(self):
        return f"{self.donor_name} - ₹{self.amount} ({self.payment_status})"


class Volunteer(models.Model):
    """Store volunteer registration information"""
    
    AVAILABILITY_CHOICES = [
        ('weekdays', 'Weekdays'),
        ('weekends', 'Weekends'),
        ('flexible', 'Flexible'),
        ('specific_days', 'Specific Days'),
    ]
    
    AREA_CHOICES = [
        ('education', 'Education'),
        ('health', 'Health'),
        ('environment', 'Environment'),
        ('community', 'Community'),
        ('admin', 'Administration'),
    ]
    
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('active', 'Active'),
        ('inactive', 'Inactive'),
    ]
    
    name = models.CharField(max_length=200)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=15)
    age = models.IntegerField(null=True, blank=True)
    address = models.TextField(blank=True)
    skills = models.TextField()
    availability = models.CharField(max_length=20, choices=AVAILABILITY_CHOICES, default='flexible')
    preferred_area = models.CharField(max_length=20, choices=AREA_CHOICES)
    experience = models.TextField(blank=True)
    message = models.TextField(blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    registration_date = models.DateTimeField(auto_now_add=True)
    approved_date = models.DateTimeField(null=True, blank=True)
    approved_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    is_active = models.BooleanField(default=True)
    newsletter_subscription = models.BooleanField(default=True)
    emergency_contact_name = models.CharField(max_length=200, blank=True)
    emergency_contact_phone = models.CharField(max_length=15, blank=True)
    
    class Meta:
        ordering = ['-registration_date']
        verbose_name = "Volunteer"
        verbose_name_plural = "Volunteers"
        indexes = [
            models.Index(fields=['email']),
            models.Index(fields=['status']),
            models.Index(fields=['registration_date']),
        ]
    
    def send_welcome_email(self):
        """Send professional HTML confirmation email to new volunteer"""
        subject = f"Welcome to {settings.SITE_CONFIG['SITE_NAME']} - Volunteer Registration"
        
        html_message = f"""
        <div style="font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; max-width: 600px; margin: 0 auto; border: 1px solid #e2e8f0; border-radius: 12px; overflow: hidden;">
            <div style="background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%); padding: 30px; text-align: center; color: white;">
                <h1 style="margin: 0; font-size: 24px;">Welcome Aboard!</h1>
                <p style="margin: 10px 0 0; opacity: 0.9;">Volunteer Registration Received</p>
            </div>
            <div style="padding: 30px; color: #1e293b; line-height: 1.6;">
                <p>Dear <strong>{self.name}</strong>,</p>
                <p>Thank you for your interest in volunteering with <strong>{settings.SITE_CONFIG['SITE_NAME']}</strong>. We are thrilled to have passionate individuals like you join our journey of empowerment.</p>
                
                <p>Your application has been successfully received and is currently being reviewed by our team. We aim to get back to you within 2-3 business days.</p>
                
                <div style="background: #f8fafc; border-radius: 8px; padding: 15px; margin: 20px 0;">
                    <p style="margin: 0; font-size: 14px; color: #64748b;"><strong>Registration Summary:</strong></p>
                    <ul style="margin: 10px 0 0; padding-left: 20px; font-size: 14px;">
                        <li><strong>Area of Interest:</strong> {self.get_preferred_area_display()}</li>
                        <li><strong>Availability:</strong> {self.get_availability_display()}</li>
                    </ul>
                </div>
                
                <p>In the meantime, feel free to explore our current projects on our website.</p>
                
                <p style="margin-top: 30px;">Best regards,<br><strong>Volunteer Coordination Team</strong><br>{settings.SITE_CONFIG['SITE_NAME']}</p>
            </div>
        </div>
        """
        
        plain_message = f"Dear {self.name}, Thank you for registering as a volunteer with {settings.SITE_CONFIG['SITE_NAME']}. Your application is under review."
        
        send_mail(
            subject, 
            plain_message, 
            settings.DEFAULT_FROM_EMAIL, 
            [self.email],
            html_message=html_message
        )
    
    def approve(self, admin_user):
        """Approve volunteer and send professional HTML notification"""
        self.status = 'approved'
        self.approved_date = timezone.now()
        self.approved_by = admin_user
        self.save()
        
        subject = f"Application Approved! - {settings.SITE_CONFIG['SITE_NAME']}"
        
        html_message = f"""
        <div style="font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; max-width: 600px; margin: 0 auto; border: 1px solid #e2e8f0; border-radius: 12px; overflow: hidden;">
            <div style="background: linear-gradient(135deg, #00b09b 0%, #96c93d 100%); padding: 30px; text-align: center; color: white;">
                <h1 style="margin: 0; font-size: 24px;">Application Approved</h1>
                <p style="margin: 10px 0 0; opacity: 0.9;">Join the movement today</p>
            </div>
            <div style="padding: 30px; color: #1e293b; line-height: 1.6;">
                <p>Dear <strong>{self.name}</strong>,</p>
                <p>Great news! Your volunteer application with <strong>{settings.SITE_CONFIG['SITE_NAME']}</strong> has been <strong>approved</strong>.</p>
                
                <p>We are excited to have you on board. Our team will reach out to you shortly with details regarding your orientation and first assignment.</p>
                
                <p>Thank you for choosing to dedicate your time and skills to make a real difference in the community.</p>
                
                <p style="margin-top: 30px;">Welcome to the family,<br><strong>Team {settings.SITE_CONFIG['SITE_NAME']}</strong></p>
            </div>
        </div>
        """
        
        plain_message = f"Dear {self.name}, Great news! Your volunteer application has been approved. Welcome to the team!"
        
        send_mail(
            subject, 
            plain_message, 
            settings.DEFAULT_FROM_EMAIL, 
            [self.email],
            html_message=html_message
        )
    
    def __str__(self):
        return f"{self.name} - {self.get_status_display()}"


class ContactSubmission(models.Model):
    """Store contact form inquiries"""
    
    name = models.CharField(max_length=200)
    email = models.EmailField()
    phone = models.CharField(max_length=15, blank=True)
    subject = models.CharField(max_length=300)
    message = models.TextField()
    submitted_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)
    is_replied = models.BooleanField(default=False)
    replied_at = models.DateTimeField(null=True, blank=True)
    admin_notes = models.TextField(blank=True)
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    
    class Meta:
        ordering = ['-submitted_at']
        verbose_name = "Contact Submission"
        verbose_name_plural = "Contact Submissions"
        indexes = [
            models.Index(fields=['is_read']),
            models.Index(fields=['submitted_at']),
            models.Index(fields=['email']),
        ]
    
    def mark_as_read(self):
        """Update is_read flag"""
        self.is_read = True
        self.save()
    
    def send_auto_reply(self):
        """Send acknowledgment email"""
        from .models import SiteSettings
        site_settings = SiteSettings.get_settings()
        site_name = site_settings.homepage_hero_title or settings.SITE_CONFIG.get('SITE_NAME')
        admin_email = site_settings.contact_email or settings.SITE_CONFIG.get('CONTACT_EMAIL')
        subject = f"Thank you for contacting {site_name}"
        message = f"""
Dear {self.name},

Thank you for reaching out to us. We have received your message and will respond as soon as possible.

Your Message:
Subject: {self.subject}
{self.message}

Best regards,
{site_name}
{admin_email}
        """
        send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [self.email])
    
    def __str__(self):
        return f"{self.subject} - {self.name}"


class TeamMember(models.Model):
    """Manage NGO team member profiles"""
    
    name = models.CharField(max_length=200)
    position = models.CharField(max_length=200)
    photo = models.ImageField(upload_to='team_photos/', blank=True, null=True)
    bio = models.TextField()
    email = models.EmailField(blank=True)
    phone = models.CharField(max_length=15, blank=True)
    social_media_links = models.JSONField(default=dict, blank=True)
    display_order = models.IntegerField(default=0)
    is_active = models.BooleanField(default=True)
    joined_date = models.DateField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['display_order', 'name']
        verbose_name = "Team Member"
        verbose_name_plural = "Team Members"
    
    def get_photo_url(self):
        """Return full URL for photo"""
        if self.photo:
            return self.photo.url
        return '/static/images/default-avatar.png'
    
    def __str__(self):
        return f"{self.name} - {self.position}"


class WorkProject(models.Model):
    """Showcase NGO's completed and ongoing work"""
    
    CATEGORY_CHOICES = [
        ('education', 'Education'),
        ('health', 'Health'),
        ('environment', 'Environment'),
        ('women_empowerment', 'Women Empowerment'),
        ('child_welfare', 'Child Welfare'),
        ('community', 'Community'),
        ('other', 'Other'),
    ]
    
    STATUS_CHOICES = [
        ('planning', 'Planning'),
        ('ongoing', 'Ongoing'),
        ('completed', 'Completed'),
        ('paused', 'Paused'),
    ]
    
    title = models.CharField(max_length=300)
    slug = models.SlugField(unique=True, blank=True)
    description = models.TextField()
    short_description = models.CharField(max_length=500)
    featured_image = models.ImageField(upload_to='work_projects/', blank=True, null=True)
    category = models.CharField(max_length=30, choices=CATEGORY_CHOICES)
    project_status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='ongoing')
    start_date = models.DateField()
    end_date = models.DateField(null=True, blank=True)
    location = models.CharField(max_length=300)
    beneficiaries_count = models.IntegerField(null=True, blank=True)
    budget = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    partners = models.TextField(blank=True)
    is_featured = models.BooleanField(default=False)
    is_published = models.BooleanField(default=True)
    views_count = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-start_date', '-created_at']
        verbose_name = "Work Project"
        verbose_name_plural = "Work Projects"
        indexes = [
            models.Index(fields=['slug']),
            models.Index(fields=['category']),
            models.Index(fields=['is_featured']),
            models.Index(fields=['is_published']),
        ]
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)
    
    def increment_views(self):
        """Increase view count"""
        self.views_count += 1
        self.save(update_fields=['views_count'])
    
    def get_absolute_url(self):
        """Return detail page URL"""
        from django.urls import reverse
        return reverse('project_detail', kwargs={'slug': self.slug})
    
    def __str__(self):
        return self.title


class ProjectGallery(models.Model):
    """Store multiple images for each work project"""
    
    project = models.ForeignKey(WorkProject, related_name='gallery_images', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='project_gallery/')
    caption = models.CharField(max_length=300, blank=True)
    display_order = models.IntegerField(default=0)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['display_order', 'uploaded_at']
        verbose_name = "Project Gallery Image"
        verbose_name_plural = "Project Gallery Images"
    
    def get_image_url(self):
        """Return full URL for image"""
        if self.image:
            return self.image.url
        return ''
    
    def __str__(self):
        return f"{self.project.title} - {self.image.name}"


class MediaGallery(models.Model):
    """General media gallery for photos and videos"""
    
    MEDIA_TYPE_CHOICES = [
        ('image', 'Image'),
        ('video', 'Video'),
    ]
    
    CATEGORY_CHOICES = [
        ('events', 'Events'),
        ('activities', 'Activities'),
        ('workshops', 'Workshops'),
        ('achievements', 'Achievements'),
        ('other', 'Other'),
    ]
    
    title = models.CharField(max_length=300)
    media_type = models.CharField(max_length=10, choices=MEDIA_TYPE_CHOICES)
    image = models.ImageField(upload_to='media_gallery/', blank=True, null=True)
    video_url = models.URLField(blank=True, null=True)
    caption = models.TextField(blank=True)
    event_date = models.DateField(null=True, blank=True)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    is_featured = models.BooleanField(default=False)
    display_order = models.IntegerField(default=0)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    uploaded_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    
    class Meta:
        ordering = ['-event_date', '-uploaded_at']
        verbose_name = "Media Item"
        verbose_name_plural = "Media Gallery"
        indexes = [
            models.Index(fields=['media_type']),
            models.Index(fields=['category']),
            models.Index(fields=['is_featured']),
        ]
    
    def get_thumbnail_url(self):
        """Return thumbnail for videos or image preview"""
        if self.media_type == 'image' and self.image:
            return self.image.url
        elif self.media_type == 'video' and self.video_url:
            # Extract YouTube thumbnail if it's a YouTube video
            if 'youtube.com' in self.video_url or 'youtu.be' in self.video_url:
                video_id = self.video_url.split('/')[-1].split('=')[-1].split('&')[0]
                return f"https://img.youtube.com/vi/{video_id}/maxresdefault.jpg"
        return '/static/images/default-media.png'
    
    def __str__(self):
        return f"{self.title} ({self.media_type})"


class SliderImage(models.Model):
    """Manage homepage slider images"""
    
    title = models.CharField(max_length=200, help_text="Optional title for the slide")
    image = models.ImageField(upload_to='slider_images/', help_text="Upload slider image (recommended: 1920x1080px)")
    caption = models.CharField(max_length=300, blank=True, help_text="Optional caption text")
    display_order = models.IntegerField(default=0, help_text="Order of appearance (lower numbers first)")
    is_active = models.BooleanField(default=True, help_text="Show this slide on homepage")
    link_url = models.URLField(blank=True, help_text="Optional link when slide is clicked")
    uploaded_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['display_order', 'uploaded_at']
        verbose_name = "Slider Image"
        verbose_name_plural = "Slider Images"
    
    def get_image_url(self):
        """Return full URL for image"""
        if self.image:
            return self.image.url
        return '/static/images/default-slider.jpg'
    
    def __str__(self):
        return self.title or f"Slide {self.display_order}"


class SiteStatistics(models.Model):
    """Dynamic statistics for homepage display"""
    
    total_beneficiaries = models.IntegerField(default=0, help_text="Total number of people benefited")
    completed_projects = models.IntegerField(default=0, help_text="Number of completed projects")
    years_of_service = models.IntegerField(default=0, help_text="Years of service")
    total_volunteers = models.IntegerField(default=0, help_text="Total active volunteers")
    total_donations = models.DecimalField(max_digits=15, decimal_places=2, default=0, help_text="Total donations received")
    updated_at = models.DateTimeField(auto_now=True)
    updated_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    
    class Meta:
        verbose_name = "Site Statistics"
        verbose_name_plural = "Site Statistics"
    
    def save(self, *args, **kwargs):
        """Override to ensure only one record exists"""
        self.pk = 1
        super().save(*args, **kwargs)
    
    def delete(self, *args, **kwargs):
        """Prevent deletion"""
        pass
    
    @classmethod
    def get_statistics(cls):
        """Return the single statistics instance"""
        obj, created = cls.objects.get_or_create(pk=1)
        return obj
    
    def __str__(self):
        return "Site Statistics"


class SiteSettings(models.Model):
    """Dynamic site configuration manageable from admin"""
    
    about_overview = models.TextField(default='')
    mission_statement = models.TextField(default='')
    vision_statement = models.TextField(default='')
    achievements_summary = models.TextField(default='')
    total_beneficiaries = models.IntegerField(default=0)
    total_projects = models.IntegerField(default=0)
    established_year = models.IntegerField(default=2020)
    registration_number = models.CharField(max_length=100, blank=True)

    # Customizable homepage content
    homepage_hero_title = models.CharField(max_length=200, default='Shree Brijwasi Jatav Samaj Sewa Samiti')
    homepage_hero_subtitle = models.CharField(max_length=300, default='Journey of Empowerment and Impact')
    donation_appeal_text = models.TextField(default='Your contribution helps us make a difference')
    volunteer_appeal_text = models.TextField(default='Join our team of dedicated volunteers')
    footer_about_text = models.TextField(default='')

    # Contact & social media (admin editable)
    contact_email = models.EmailField(blank=True, help_text="Primary contact email displayed on site")
    contact_phone = models.CharField(max_length=20, blank=True, help_text="Primary contact phone number")
    contact_address = models.CharField(max_length=300, blank=True, help_text="Physical address of the organization")
    social_media_links = models.JSONField(default=dict, blank=True, help_text="JSON object with social media URLs, e.g. {'facebook':'...','twitter':'...'}")

    # Optional payment override
    donation_upi_vpa = models.CharField(max_length=100, blank=True, help_text="UPI ID to override PAYMENT_CONFIG for donations")

    # SEO fields
    meta_description = models.CharField(max_length=160, blank=True)
    meta_keywords = models.CharField(max_length=300, blank=True)
    updated_at = models.DateTimeField(auto_now=True)
    updated_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    
    class Meta:
        verbose_name = "Site Settings"
        verbose_name_plural = "Site Settings"
    
    def save(self, *args, **kwargs):
        """Override to ensure only one record exists"""
        self.pk = 1
        super().save(*args, **kwargs)
    
    def delete(self, *args, **kwargs):
        """Prevent deletion"""
        pass
    
    @classmethod
    def get_settings(cls):
        """Return the single settings instance

        When the record is first created or when new fields are added, populate
        blank values from the static configuration to avoid empty renderings in
        templates. This makes the admin record usable immediately.
        """
        obj, created = cls.objects.get_or_create(pk=1)
        changed = False
        # fill any new fields from settings if empty
        if not obj.contact_email:
            obj.contact_email = settings.SITE_CONFIG.get('CONTACT_EMAIL', '')
            changed = True
        if not obj.contact_phone:
            obj.contact_phone = settings.SITE_CONFIG.get('CONTACT_PHONE', '')
            changed = True
        if not obj.contact_address:
            obj.contact_address = settings.SITE_CONFIG.get('CONTACT_ADDRESS', '')
            changed = True
        if not obj.social_media_links:
            obj.social_media_links = settings.SITE_CONFIG.get('SOCIAL_MEDIA', {})
            changed = True
        if not obj.donation_upi_vpa:
            obj.donation_upi_vpa = settings.PAYMENT_CONFIG.get('UPI_VPA', '')
            changed = True
        if changed:
            obj.save()
        return obj
    
    def __str__(self):
        return "Site Settings"
