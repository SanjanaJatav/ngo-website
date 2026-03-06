"""
Views for NGO website
Single-file-per-page view architecture as per PRD
"""

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Sum, Q
from django.conf import settings
from django.utils import timezone
from django.http import JsonResponse
from .models import (
    Donation, Volunteer, ContactSubmission, TeamMember,
    WorkProject, ProjectGallery, MediaGallery, SiteSettings,
    SliderImage, SiteStatistics
)
import urllib.parse
import logging

# Set up logger
logger = logging.getLogger(__name__)



def home_view(request):
    """
    Home page view
    GET: Display homepage with slider, statistics, featured projects
    """
    # Get site settings
    site_settings = SiteSettings.get_settings()
    
    # Get active slider images
    slider_images = SliderImage.objects.filter(is_active=True).order_by('display_order')
    
    # Get site statistics
    site_statistics = SiteStatistics.get_statistics()
    
    # Get featured projects
    featured_projects = WorkProject.objects.filter(
        is_featured=True, 
        is_published=True
    ).order_by('-start_date')[:3]
    
    # Calculate dynamic statistics (fallback to database values)
    total_donations = Donation.objects.filter(payment_status='completed').aggregate(
        total=Sum('amount')
    )['total'] or site_statistics.total_donations
    
    total_volunteers = Volunteer.objects.filter(is_active=True).count() or site_statistics.total_volunteers
    
    total_beneficiaries = site_statistics.total_beneficiaries or site_settings.total_beneficiaries
    
    completed_projects = WorkProject.objects.filter(
        project_status='completed'
    ).count() or site_statistics.completed_projects
    
    # Calculate years of service
    current_year = timezone.now().year
    years_of_service = site_statistics.years_of_service or (current_year - site_settings.established_year)
    
    # Recent updates (latest projects or media)
    recent_updates = WorkProject.objects.filter(
        is_published=True
    ).order_by('-created_at')[:3]
    
    context = {
        'site_settings': site_settings,
        'slider_images': slider_images,
        'featured_projects': featured_projects,
        'statistics': {
            'total_donations': total_donations,
            'total_volunteers': total_volunteers,
            'total_beneficiaries': total_beneficiaries,
            'completed_projects': completed_projects,
            'years_of_service': years_of_service,
        },
        'donation_appeal': site_settings.donation_appeal_text,
        'volunteer_appeal': site_settings.volunteer_appeal_text,
        'recent_updates': recent_updates,
        'page_title': 'Home',
    }
    
    return render(request, 'home.html', context)


def about_overview_view(request):
    """
    About Us Overview page view
    GET: Display mission, vision, overview information
    """
    site_settings = SiteSettings.get_settings()
    
    # Calculate years of operation
    current_year = timezone.now().year
    years_of_operation = current_year - site_settings.established_year
    
    context = {
        'site_settings': site_settings,
        'years_of_operation': years_of_operation,
        'page_title': 'About Us - Overview',
        'meta_description': site_settings.meta_description,
    }
    
    return render(request, 'about_overview.html', context)


def team_view(request):
    """
    Our Team page view
    GET: Display all team members
    """
    # Separate leadership positions from general members
    leadership_positions = ['President', 'Vice President', 'Secretary', 'Treasurer']
    
    leadership = TeamMember.objects.filter(
        is_active=True,
        position__in=leadership_positions
    ).order_by('display_order', 'name')
    
    team_members = TeamMember.objects.filter(
        is_active=True
    ).exclude(
        position__in=leadership_positions
    ).order_by('display_order', 'name')
    
    context = {
        'leadership': leadership,
        'team_members': team_members,
        'page_title': 'Our Team',
        'meta_description': 'Meet the dedicated team behind Shree Brijwasi Jatav Samaj Sewa Samiti',
    }
    
    return render(request, 'team.html', context)


def our_work_view(request):
    """
    Our Work page view
    GET: Display all projects with filtering and pagination
    """
    # Get filter parameters
    category = request.GET.get('category', 'all')
    status = request.GET.get('status', 'all')
    
    # Build query
    projects = WorkProject.objects.filter(is_published=True)
    
    if category != 'all':
        projects = projects.filter(category=category)
    
    if status != 'all':
        projects = projects.filter(project_status=status)
    
    projects = projects.order_by('-start_date')
    
    # Calculate aggregate statistics
    total_completed = WorkProject.objects.filter(
        project_status='completed'
    ).count()
    
    total_beneficiaries = WorkProject.objects.filter(
        project_status='completed',
        beneficiaries_count__isnull=False
    ).aggregate(total=Sum('beneficiaries_count'))['total'] or 0
    
    ongoing_projects = WorkProject.objects.filter(
        project_status='ongoing'
    ).count()
    
    # Pagination
    paginator = Paginator(projects, 12)  # 12 projects per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'projects': page_obj,
        'categories': WorkProject.CATEGORY_CHOICES,
        'selected_category': category,
        'selected_status': status,
        'statistics': {
            'total_completed': total_completed,
            'total_beneficiaries': total_beneficiaries,
            'ongoing_projects': ongoing_projects,
        },
        'page_obj': page_obj,
        'page_title': 'Our Work',
    }
    
    return render(request, 'our_work.html', context)


def project_detail_view(request, slug):
    """
    Work Project Detail page view
    GET: Display detailed information about a single project
    """
    # Get project
    project = get_object_or_404(WorkProject, slug=slug, is_published=True)
    
    # Increment view count
    project.increment_views()
    
    # Get project gallery images
    gallery_images = project.gallery_images.all()
    
    # Get related projects (same category)
    related_projects = WorkProject.objects.filter(
        category=project.category,
        is_published=True
    ).exclude(id=project.id).order_by('-start_date')[:3]
    
    context = {
        'project': project,
        'gallery_images': gallery_images,
        'related_projects': related_projects,
        'page_title': project.title,
        'meta_description': project.short_description,
    }
    
    return render(request, 'project_detail.html', context)


def donate_view(request):
    """
    Donation page view
    GET: Display donation form
    POST: Process donation and redirect to UPI app
    """
    # site settings available for dynamic contact/payment values
    site_settings = SiteSettings.get_settings()

    if request.method == 'POST':
        # Get form data
        donor_name = request.POST.get('donor_name', '').strip()
        donor_email = request.POST.get('donor_email', '').strip()
        donor_phone = request.POST.get('donor_phone', '').strip()
        amount = request.POST.get('amount', '').strip()
        payment_app = request.POST.get('payment_app', '').strip()
        donation_purpose = request.POST.get('donation_purpose', '')
        is_anonymous = request.POST.get('is_anonymous') == 'on'
        
        # Validate required fields
        if not donor_name:
            messages.error(request, 'Please enter your full name.')
            return redirect('donate')
        if not donor_email:
            messages.error(request, 'Please enter your email address.')
            return redirect('donate')
        if not amount:
            messages.error(request, 'Please select a donation amount.')
            return redirect('donate')
        if not payment_app:
            messages.error(request, 'Please select a payment method.')
            return redirect('donate')
        
        # Validate amount
        try:
            amount = float(amount)
            if amount < settings.PAYMENT_CONFIG['MINIMUM_DONATION']:
                messages.error(request, f"Minimum donation amount is ₹{settings.PAYMENT_CONFIG['MINIMUM_DONATION']}")
                return redirect('donate')
        except ValueError:
            messages.error(request, "Invalid amount. Please enter a valid number.")
            return redirect('donate')
        
        # Create donation record
        donation = Donation.objects.create(
            donor_name=donor_name,
            donor_email=donor_email,
            donor_phone=donor_phone,
            amount=amount,
            payment_app=payment_app,
            donation_purpose=donation_purpose,
            is_anonymous=is_anonymous,
            payment_status='pending'
        )
        
        logger.info(f"Donation initiated: {donation.transaction_reference} for ₹{amount} by {donor_email}")

        
        # Build UPI deep link
        upi_vpa = site_settings.donation_upi_vpa or settings.PAYMENT_CONFIG['UPI_VPA']
        payee_name = settings.PAYMENT_CONFIG['UPI_PAYEE_NAME']
        transaction_ref = donation.transaction_reference
        
        # Base UPI URL
        upi_params = {
            'pa': upi_vpa,
            'pn': payee_name,
            'am': str(amount),
            'tn': transaction_ref,
            'cu': 'INR'
        }
        
        upi_url = f"upi://pay?{urllib.parse.urlencode(upi_params)}"
        
        # App-specific deep links
        app_links = {
            'googlepay': f"tez://upi/pay?{urllib.parse.urlencode(upi_params)}",
            'phonepe': f"phonepe://pay?{urllib.parse.urlencode(upi_params)}",
            'paytm': f"paytmmp://pay?{urllib.parse.urlencode(upi_params)}",
            'bhim': upi_url,
            'other': upi_url,
        }
        
        deep_link = app_links.get(payment_app, upi_url)
        
        # Store in session
        request.session['donation_id'] = donation.id
        request.session['deep_link'] = deep_link
        
        # Send notification email to admin
        from django.core.mail import send_mail
        admin_email = site_settings.contact_email or settings.SITE_CONFIG.get('CONTACT_EMAIL')
        send_mail(
            'New Donation Pending Verification',
            f'New donation of ₹{amount} from {donor_name} ({donor_email})\nTransaction Reference: {transaction_ref}',
            settings.DEFAULT_FROM_EMAIL,
            [admin_email],
            fail_silently=True,
        )
        
        # Send confirmation to donor
        site_name = site_settings.homepage_hero_title or settings.SITE_CONFIG.get('SITE_NAME')
        send_mail(
            f"Thank you for your donation - {site_name}",
            f'''Dear {donor_name},

Thank you for initiating a donation of ₹{amount} to {site_name}.

Transaction Reference: {transaction_ref}
Status: Pending Verification

Please complete the payment in your UPI app. Once verified by our team, you will receive a receipt via email.

Best regards,
{site_name}''',
            settings.DEFAULT_FROM_EMAIL,
            [donor_email],
            fail_silently=True,
        )
        
        return redirect('donation_thank_you')
    
    # GET request
    recent_donors = Donation.objects.filter(
        payment_status='completed',
        is_anonymous=False
    ).order_by('-completed_at')[:10]
    
    # compute dynamic payment settings (mirror context processor logic)
    dynamic_payment = settings.PAYMENT_CONFIG.copy()
    if site_settings.donation_upi_vpa:
        dynamic_payment['UPI_VPA'] = site_settings.donation_upi_vpa

    context = {
        'recent_donors': recent_donors,
        'minimum_donation': dynamic_payment['MINIMUM_DONATION'],
        'suggested_amounts': [500, 1000, 2000, 5000, 10000],
        'upi_apps': dynamic_payment['SUPPORTED_UPI_APPS'],
        'upi_vpa': dynamic_payment['UPI_VPA'],
        'page_title': 'Donate Now',
    }
    
    return render(request, 'donate.html', context)


def donation_thank_you_view(request):
    """
    Donation thank you page
    """
    donation_id = request.session.get('donation_id')
    deep_link = request.session.get('deep_link')
    
    donation = None
    if donation_id:
        try:
            donation = Donation.objects.get(id=donation_id)
        except Donation.DoesNotExist:
            pass
    
    context = {
        'donation': donation,
        'deep_link': deep_link,
        'page_title': 'Thank You for Your Donation',
    }
    
    return render(request, 'donation_thank_you.html', context)


def media_view(request):
    """
    Media Gallery page view
    GET: Display photos and videos with filtering
    """
    # Get filter parameters
    category = request.GET.get('category', 'all')
    media_type = request.GET.get('media_type', 'all')
    
    # Build query
    media_items = MediaGallery.objects.all()
    
    if category != 'all':
        media_items = media_items.filter(category=category)
    
    if media_type != 'all':
        media_items = media_items.filter(media_type=media_type)
    
    media_items = media_items.order_by('-event_date', '-uploaded_at')
    
    # Pagination
    paginator = Paginator(media_items, 24)  # 24 items per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'media_items': page_obj,
        'categories': MediaGallery.CATEGORY_CHOICES,
        'selected_category': category,
        'selected_media_type': media_type,
        'page_obj': page_obj,
        'page_title': 'Media Gallery',
    }
    
    return render(request, 'media.html', context)


def contact_view(request):
    """
    Contact page view
    GET: Display contact form
    POST: Process contact form submission
    """
    if request.method == 'POST':
        # Get form data
        name = request.POST.get('name')
        email = request.POST.get('email')
        phone = request.POST.get('phone', '')
        subject = request.POST.get('subject')
        message_text = request.POST.get('message')
        
        # Get IP address
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip_address = x_forwarded_for.split(',')[0]
        else:
            ip_address = request.META.get('REMOTE_ADDR')
        
        # Create submission
        submission = ContactSubmission.objects.create(
            name=name,
            email=email,
            phone=phone,
            subject=subject,
            message=message_text,
            ip_address=ip_address
        )
        
        logger.info(f"Contact form submitted by {email} from IP {ip_address}")

        
        # Send notification to admin
        from django.core.mail import send_mail
        send_mail(
            f'New Contact Form Submission: {subject}',
            f'''New contact form submission from {name}

Email: {email}
Phone: {phone}
Subject: {subject}

Message:
{message_text}''',
            settings.DEFAULT_FROM_EMAIL,
            [settings.SITE_CONFIG['CONTACT_EMAIL']],
            fail_silently=True,
        )
        
        # Send auto-reply to user
        submission.send_auto_reply()
        
        messages.success(request, 'Thank you for contacting us! We will respond shortly.')
        return redirect('contact')
    
    # GET request
    context = {
        'page_title': 'Contact Us',
    }
    
    return render(request, 'contact.html', context)


def volunteer_view(request):
    """
    Volunteer registration page view
    GET: Display volunteer form
    POST: Process volunteer registration
    """
    if request.method == 'POST':
        # Get form data
        name = request.POST.get('name', '').strip()
        email = request.POST.get('email', '').strip()
        phone = request.POST.get('phone', '').strip()
        age = request.POST.get('age', None)
        address = request.POST.get('address', '').strip()
        skills = request.POST.get('skills', '').strip()
        availability = request.POST.get('availability', '').strip()
        preferred_area = request.POST.get('preferred_area', '').strip()
        experience = request.POST.get('experience', '').strip()
        message = request.POST.get('message', '').strip()
        emergency_contact_name = request.POST.get('emergency_contact_name', '').strip()
        emergency_contact_phone = request.POST.get('emergency_contact_phone', '').strip()
        
        # Validate required fields
        if not name:
            messages.error(request, 'Please provide your full name.')
            return redirect('volunteer')
        if not email:
            messages.error(request, 'Please provide your email address.')
            return redirect('volunteer')
        if not phone:
            messages.error(request, 'Please provide your phone number.')
            return redirect('volunteer')
        if not skills:
            messages.error(request, 'Please tell us about your skills and expertise.')
            return redirect('volunteer')
        if not preferred_area:
            messages.error(request, 'Please select your preferred area.')
            return redirect('volunteer')
        if not availability:
            messages.error(request, 'Please select your availability.')
            return redirect('volunteer')
        
        # Check for duplicate email
        if Volunteer.objects.filter(email=email).exists():
            messages.error(request, 'This email is already registered as a volunteer.')
            return redirect('volunteer')
        
        # Create volunteer record
        volunteer = Volunteer.objects.create(
            name=name,
            email=email,
            phone=phone,
            age=int(age) if age else None,
            address=address,
            skills=skills,
            availability=availability,
            preferred_area=preferred_area,
            experience=experience,
            message=message,
            emergency_contact_name=emergency_contact_name,
            emergency_contact_phone=emergency_contact_phone,
            status='pending'
        )
        
        logger.info(f"New volunteer registered: {email} for {preferred_area}")

        
        # Send welcome email
        volunteer.send_welcome_email()
        
        # Send notification to admin
        from django.core.mail import send_mail
        send_mail(
            'New Volunteer Registration',
            f'''New volunteer registration:

Name: {name}
Email: {email}
Phone: {phone}
Preferred Area: {volunteer.get_preferred_area_display()}
Skills: {skills}

Please review and approve in the admin panel.''',
            settings.DEFAULT_FROM_EMAIL,
            [settings.SITE_CONFIG['CONTACT_EMAIL']],
            fail_silently=True,
        )
        
        return redirect('volunteer_thank_you')
    
    # GET request
    context = {
        'availability_choices': Volunteer.AVAILABILITY_CHOICES,
        'area_choices': Volunteer.AREA_CHOICES,
        'page_title': 'Become a Volunteer',
    }
    
    return render(request, 'volunteer.html', context)


def volunteer_thank_you_view(request):
    """
    Volunteer registration thank you page
    """
    context = {
        'page_title': 'Thank You for Volunteering',
    }
    
    return render(request, 'volunteer_thank_you.html', context)
