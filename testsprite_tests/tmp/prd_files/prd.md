Product Requirements Document (PRD)
Shree Brijwasi Jatav Samaj Sewa Samiti - NGO Website

1. Project Overview
1.1 Project Name
Shree Brijwasi Jatav Samaj Sewa Samiti Official Website
1.2 Project Type
Full-stack NGO web application with donation system and volunteer management
1.3 Project Description
This project is a comprehensive web platform for an NGO dedicated to social empowerment and community service. The website will serve as the primary digital presence for Shree Brijwasi Jatav Samaj Sewa Samiti, enabling them to showcase their mission, attract volunteers, receive donations through UPI payment systems, and engage with the community. The platform emphasizes simplicity in codebase management while maintaining professional functionality and security standards.
1.4 Core Objectives

Establish strong online presence for the NGO
Enable seamless online donations through UPI payment integration
Facilitate volunteer registration and management
Showcase NGO's work, team, and impact
Provide easy content management for NGO administrators
Ensure fast page load times (≤3 seconds for homepage)
Support deployment from localhost to production without code changes


2. Technical Architecture
2.1 Technology Stack
Frontend Technologies

HTML5: Semantic markup for content structure
CSS3: Styling with custom properties for theme management
JavaScript (ES6+): Interactive features, image slider, form validations
Bootstrap 5: Responsive grid system and UI components

Backend Framework

Django 4.2+: Python web framework for server-side logic
Django ORM: Database abstraction layer for MySQL interactions
Django Template Engine: Server-side rendering with template inheritance

Database

MySQL 8.0+: Relational database for all data storage
Django Migrations: Version control for database schema

Development Environment

XAMPP: Local development server (Apache + MySQL + PHP, though PHP not used)
Django Development Server: Running on localhost:8000
Python 3.9+: Runtime environment

Production Environment

cPanel Hosting: Shared hosting with Python support
Apache/Passenger: WSGI application server
MySQL Database: cPanel-managed database instance

Payment Integration

UPI Deep Links: Google Pay, PhonePe, Paytm, BHIM integration
Manual Payment Verification: Admin-verified donation confirmation

2.2 Architecture Pattern
Single-File-Per-Page View Architecture
Each page functionality is consolidated into a single view function that handles:

GET requests: Rendering the template with context data
POST requests: Processing form submissions and database operations
Business logic: Validation, payment processing, email notifications
Error handling: Form errors, database exceptions, payment failures

Django MTV Pattern Implementation

Models: Define database schema for all entities
Templates: HTML files with Django template language for dynamic content
Views: Python functions handling request/response cycle for each page

Configuration-Driven Deployment

Central configuration file manages all environment-specific settings
Single file update enables deployment from localhost to production
No code changes required during deployment process


3. System Architecture Design
3.1 Configuration Management System
Configuration File Structure (config/config.py)
The configuration system uses a Python module with distinct sections:
Database Configuration Section
DATABASE_CONFIG dictionary containing:
- ENGINE: MySQL backend driver
- NAME: Database name (different for localhost and cPanel)
- USER: Database username
- PASSWORD: Database password
- HOST: Database host (localhost or cPanel-provided host)
- PORT: MySQL port (typically 3306)
- OPTIONS: Additional MySQL connection parameters
Site Configuration Section
SITE_CONFIG dictionary containing:
- SITE_NAME: "Shree Brijwasi Jatav Samaj Sewa Samiti"
- SITE_TAGLINE: Organizational tagline
- LOGO_PATH: Path to logo file in static directory
- LOGO_PRIMARY_COLOR: Hex color code extracted from logo
- LOGO_SECONDARY_COLOR: Accent color from logo
- LOGO_BACKGROUND_COLOR: Background theme color
- CONTACT_EMAIL: Official NGO email
- CONTACT_PHONE: Contact number
- CONTACT_ADDRESS: Physical address
- SOCIAL_MEDIA: Dictionary with Facebook, Twitter, Instagram, YouTube links
Payment Configuration Section
PAYMENT_CONFIG dictionary containing:
- UPI_VPA: NGO's UPI Virtual Payment Address
- UPI_PAYEE_NAME: Beneficiary name for UPI transactions
- SUPPORTED_UPI_APPS: List of integrated UPI applications
- MINIMUM_DONATION: Minimum donation amount
- CURRENCY: INR
- TRANSACTION_PREFIX: Unique identifier prefix for tracking
Email Configuration Section
EMAIL_CONFIG dictionary containing:
- EMAIL_BACKEND: SMTP backend
- EMAIL_HOST: SMTP server address
- EMAIL_PORT: SMTP port
- EMAIL_USE_TLS: Security setting
- EMAIL_HOST_USER: Sender email
- EMAIL_HOST_PASSWORD: Email password
- DEFAULT_FROM_EMAIL: Display name and email
Media Configuration Section
MEDIA_CONFIG dictionary containing:
- UPLOAD_PATHS: Subdirectories for different media types
- ALLOWED_IMAGE_TYPES: jpg, jpeg, png, webp, gif
- ALLOWED_VIDEO_TYPES: mp4, webm
- MAX_IMAGE_SIZE: Maximum file size in MB
- MAX_VIDEO_SIZE: Maximum file size in MB
- IMAGE_COMPRESSION_QUALITY: Quality setting for uploaded images
Slider Configuration Section
SLIDER_CONFIG dictionary containing:
- SLIDER_IMAGES: List of background image paths
- SLIDER_INTERVAL: Time between slides in milliseconds
- SLIDER_TRANSITION: Animation type (fade, slide)
- SLIDER_AUTOPLAY: Boolean for automatic rotation
Configuration Import in Django Settings
The main settings.py file imports configuration:
Import config module
Load DATABASE_CONFIG into DATABASES setting
Load EMAIL_CONFIG into email settings
Make SITE_CONFIG, PAYMENT_CONFIG accessible globally
Set STATIC_ROOT, MEDIA_ROOT based on environment
Configure DEBUG based on environment (True for localhost, False for cPanel)
Set ALLOWED_HOSTS from config
Environment Detection
The system automatically detects environment:
Check if running on localhost (127.0.0.1 or localhost in hostname)
Check if running on cPanel (domain name in hostname)
Load appropriate configuration section
Set environment-specific paths for static and media files
3.2 Single-File-Per-Page View Implementation
View Function Structure
Each page view follows this pattern:
Function name corresponds to page (e.g., home_view, about_view, donate_view)
Accept request object as parameter
Check request method (GET or POST)

IF GET request:
    Fetch required data from database using ORM queries
    Prepare context dictionary with data
    Render template with context
    Return HTTP response

IF POST request:
    Validate form data using Django forms
    Check CSRF token automatically by Django
    Process data (save to database, send email, redirect to payment)
    Handle errors and validation failures
    Redirect to success page or re-render with errors
    Return HTTP response
Example View Patterns
Home Page View Pattern:
Query recent work projects (limit 3)
Query team member count
Query total donations received
Query volunteer count
Load slider images from config
Prepare context with all data
Render home.html template
Donation Page View Pattern:
IF GET:
    Show donation form with UPI options
    Load payment config for display

IF POST:
    Validate amount, donor details
    Generate unique transaction reference
    Create donation record with pending status
    Build UPI deep link with VPA, amount, transaction reference
    Save transaction to database
    Redirect user to selected UPI app
    Provide callback URL for confirmation
Volunteer Registration View Pattern:
IF GET:
    Display volunteer registration form

IF POST:
    Validate all form fields (name, email, phone, skills, message)
    Check for duplicate email registration
    Create volunteer record in database
    Send confirmation email to volunteer
    Send notification email to NGO admin
    Redirect to thank you page with success message
Contact Page View Pattern:
IF GET:
    Show contact form with NGO details from config

IF POST:
    Validate contact form fields
    Save submission to database
    Send email notification to NGO
    Send auto-reply to user
    Redirect with success message
3.3 Template Inheritance System
Base Template Structure (templates/base.html)
The master template contains:
HTML5 DOCTYPE and language declaration
Head section:
    - Meta tags (charset, viewport, description, keywords)
    - Title tag with dynamic page title
    - Favicon link from static files
    - CSS files loading:
        - Bootstrap CSS from CDN
        - Custom styles.css with theme variables
        - Page-specific CSS block
    - Google Fonts import for typography
    
Body section:
    - Header block:
        - Logo image with dynamic path from config
        - Navigation menu with active page highlighting
        - Mobile responsive hamburger menu
    
    - Main content block (empty, filled by child templates)
    
    - Footer block:
        - NGO information from config
        - Quick links to all pages
        - Social media icons from config
        - Copyright notice
    
    - JavaScript section:
        - jQuery from CDN
        - Bootstrap JS from CDN
        - Custom main.js file
        - Page-specific JS block
Child Template Pattern
Each page template extends base:
Extend base.html
Override title block with page-specific title
Override content block with page-specific HTML
Optionally override extra_css block for page styles
Optionally override extra_js block for page scripts
Use Django template variables for dynamic content
Include template tags for loops, conditionals, filters
Reusable Component Templates
Navigation Component (includes/navigation.html):
Responsive navbar with logo
Links to all pages
Active page highlighting using Django request.path
Mobile hamburger menu toggle
Dropdown for About Us subsections
Footer Component (includes/footer.html):
Three-column layout
Column 1: About NGO summary
Column 2: Quick links
Column 3: Contact information and social media
Copyright with dynamic year
Donation Card Component (includes/donation_card.html):
Reusable card for displaying donation call-to-action
Accepts parameters: title, description, button_text
Used on home page and work pages
Team Member Card Component (includes/team_card.html):
Photo, name, position, bio
Reusable across team listing page
Accepts team member object as parameter
Responsive grid layout
3.4 Static Files Management
CSS Architecture (static/css/styles.css)
The stylesheet is organized into sections:
CSS Custom Properties section:
    - Define theme colors from config as CSS variables
    - Typography variables (font families, sizes, weights)
    - Spacing variables (margins, paddings)
    - Border radius, shadow variables
    
Global Styles section:
    - Reset and normalize styles
    - Body, html base styles
    - Typography hierarchy (h1-h6, p, links)
    - Global link styles with hover effects
    
Layout Styles section:
    - Container widths and breakpoints
    - Grid system customizations
    - Section padding and margins
    
Component Styles section:
    - Header and navigation styles
    - Footer styles
    - Button styles with theme colors
    - Card components
    - Form input styles
    - Modal styles
    
Page-Specific Styles section:
    - Home page hero slider
    - About page timeline
    - Work page gallery grid
    - Media page lightbox
    - Contact page map embed
    - Donation page payment selection
    
Utility Classes section:
    - Text utilities (colors, alignment, transforms)
    - Background utilities
    - Spacing utilities
    - Display utilities
    
Responsive Styles section:
    - Mobile breakpoint (max-width 576px)
    - Tablet breakpoint (max-width 768px)
    - Desktop breakpoint (min-width 992px)
JavaScript Architecture (static/js/main.js)
The main JavaScript file contains:
Initialization section:
    - DOM ready event listener
    - Load theme colors from data attributes
    - Initialize all interactive components

Image Slider Module:
    - Slider configuration from data attributes
    - Auto-play functionality
    - Manual navigation (prev/next buttons)
    - Indicator dots click handlers
    - Pause on hover
    - Preload images for smooth transitions
    - Fade/slide animation logic

Form Validation Module:
    - Client-side validation for all forms
    - Real-time validation on blur events
    - Email format validation
    - Phone number format validation
    - Required field checks
    - Custom error message display

Navigation Module:
    - Mobile menu toggle
    - Smooth scroll to sections
    - Active page highlighting
    - Sticky header on scroll
    - Dropdown menu interactions

Donation Module:
    - UPI app selection
    - Amount input validation
    - Dynamic deep link generation
    - Payment confirmation handling
    - Receipt display logic

Media Gallery Module:
    - Lazy loading for images
    - Lightbox functionality
    - Image zoom and pan
    - Video play in modal
    - Gallery filtering by category

Contact Form Module:
    - Form submission via AJAX
    - Success/error message display
    - Form reset after submission
    - reCAPTCHA integration (if enabled)

Utility Functions:
    - Show/hide loading spinner
    - Toast notification display
    - Scroll to top button
    - Smooth animations
    - Date formatting

4. Database Schema Design
4.1 Django Models Structure
Donations Model
Purpose: Track all donation transactions and donor information
Fields:

id: AutoField (Primary Key, auto-increment)
donor_name: CharField (max_length=200, required)
donor_email: EmailField (required, for sending receipts)
donor_phone: CharField (max_length=15, optional)
amount: DecimalField (max_digits=10, decimal_places=2, required)
upi_transaction_id: CharField (max_length=100, unique, nullable initially)
payment_app: CharField (choices for GPay, PhonePe, Paytm, BHIM, Other)
payment_status: CharField (choices: pending, completed, failed, refunded)
transaction_reference: CharField (max_length=50, unique, auto-generated)
donation_purpose: TextField (optional, donor can specify)
is_anonymous: BooleanField (default False, hide donor name publicly)
receipt_sent: BooleanField (default False, track email confirmation)
created_at: DateTimeField (auto_now_add, timestamp of donation initiation)
completed_at: DateTimeField (null, timestamp when payment confirmed)
notes: TextField (optional, admin notes)

Meta Options:

ordering: ['-created_at']
verbose_name: "Donation"
verbose_name_plural: "Donations"
indexes on: donor_email, transaction_reference, payment_status, created_at

Model Methods:

generate_transaction_reference(): Create unique reference with prefix + timestamp
send_receipt_email(): Send thank you email with receipt
mark_completed(): Update status and timestamp when payment verified
str(): Return donor name and amount for admin display

Volunteers Model
Purpose: Store volunteer registration information
Fields:

id: AutoField (Primary Key)
name: CharField (max_length=200, required)
email: EmailField (unique, required)
phone: CharField (max_length=15, required)
age: IntegerField (optional)
address: TextField (optional, for local volunteers)
skills: TextField (required, what they can contribute)
availability: CharField (choices: weekdays, weekends, flexible, specific_days)
preferred_area: CharField (choices: education, health, environment, community, admin)
experience: TextField (optional, previous volunteer work)
message: TextField (optional, why they want to volunteer)
status: CharField (choices: pending, approved, active, inactive)
registration_date: DateTimeField (auto_now_add)
approved_date: DateTimeField (null, when admin approves)
approved_by: ForeignKey (to User model, admin who approved, null)
is_active: BooleanField (default True)
newsletter_subscription: BooleanField (default True)
emergency_contact_name: CharField (max_length=200, optional)
emergency_contact_phone: CharField (max_length=15, optional)

Meta Options:

ordering: ['-registration_date']
verbose_name: "Volunteer"
verbose_name_plural: "Volunteers"
indexes on: email, status, registration_date

Model Methods:

send_welcome_email(): Send confirmation email to new volunteer
approve(): Change status to approved and send notification
str(): Return volunteer name and registration date

ContactSubmissions Model
Purpose: Store contact form inquiries
Fields:

id: AutoField (Primary Key)
name: CharField (max_length=200, required)
email: EmailField (required)
phone: CharField (max_length=15, optional)
subject: CharField (max_length=300, required)
message: TextField (required)
submitted_at: DateTimeField (auto_now_add)
is_read: BooleanField (default False)
is_replied: BooleanField (default False)
replied_at: DateTimeField (null)
admin_notes: TextField (optional, internal notes)
ip_address: GenericIPAddressField (for spam prevention)

Meta Options:

ordering: ['-submitted_at']
verbose_name: "Contact Submission"
verbose_name_plural: "Contact Submissions"
indexes on: is_read, submitted_at, email

Model Methods:

mark_as_read(): Update is_read flag
send_auto_reply(): Send acknowledgment email
str(): Return subject and submission date

TeamMembers Model
Purpose: Manage NGO team member profiles
Fields:

id: AutoField (Primary Key)
name: CharField (max_length=200, required)
position: CharField (max_length=200, required, e.g., "President", "Secretary")
photo: ImageField (upload_to='team_photos/', required)
bio: TextField (required, member background and role)
email: EmailField (optional, public contact)
phone: CharField (max_length=15, optional)
social_media_links: JSONField (optional, store multiple social links)
display_order: IntegerField (default=0, for custom sorting)
is_active: BooleanField (default True, show/hide from public)
joined_date: DateField (when they joined the organization)
created_at: DateTimeField (auto_now_add)
updated_at: DateTimeField (auto_now)

Meta Options:

ordering: ['display_order', 'name']
verbose_name: "Team Member"
verbose_name_plural: "Team Members"

Model Methods:

get_photo_url(): Return full URL for photo
str(): Return name and position

WorkProjects Model
Purpose: Showcase NGO's completed and ongoing work
Fields:

id: AutoField (Primary Key)
title: CharField (max_length=300, required)
slug: SlugField (unique, auto-generated from title for URLs)
description: TextField (required, detailed project description)
short_description: CharField (max_length=500, for listing pages)
featured_image: ImageField (upload_to='work_projects/', required)
category: CharField (choices: education, health, environment, women_empowerment, child_welfare, community, other)
project_status: CharField (choices: planning, ongoing, completed, paused)
start_date: DateField (required)
end_date: DateField (null, for ongoing projects)
location: CharField (max_length=300, where project is happening)
beneficiaries_count: IntegerField (optional, number of people impacted)
budget: DecimalField (max_digits=12, decimal_places=2, optional)
partners: TextField (optional, collaborating organizations)
is_featured: BooleanField (default False, show on homepage)
is_published: BooleanField (default True)
views_count: IntegerField (default=0, track page views)
created_at: DateTimeField (auto_now_add)
updated_at: DateTimeField (auto_now)

Meta Options:

ordering: ['-start_date', '-created_at']
verbose_name: "Work Project"
verbose_name_plural: "Work Projects"
indexes on: slug, category, is_featured, is_published

Model Methods:

increment_views(): Increase view count
get_absolute_url(): Return detail page URL
str(): Return project title

ProjectGallery Model
Purpose: Store multiple images for each work project
Fields:

id: AutoField (Primary Key)
project: ForeignKey (to WorkProjects, related_name='gallery_images', on_delete=CASCADE)
image: ImageField (upload_to='project_gallery/', required)
caption: CharField (max_length=300, optional)
display_order: IntegerField (default=0)
uploaded_at: DateTimeField (auto_now_add)

Meta Options:

ordering: ['display_order', 'uploaded_at']
verbose_name: "Project Gallery Image"
verbose_name_plural: "Project Gallery Images"

Model Methods:

get_image_url(): Return full URL for image
str(): Return project title and image filename

MediaGallery Model
Purpose: General media gallery for photos and videos
Fields:

id: AutoField (Primary Key)
title: CharField (max_length=300, required)
media_type: CharField (choices: image, video)
image: ImageField (upload_to='media_gallery/', null if video)
video_url: URLField (null if image, YouTube/Vimeo embed link)
caption: TextField (optional)
event_date: DateField (optional, when photo/video was taken)
category: CharField (choices: events, activities, workshops, achievements, other)
is_featured: BooleanField (default False)
display_order: IntegerField (default=0)
uploaded_at: DateTimeField (auto_now_add)
uploaded_by: ForeignKey (to User model, admin who uploaded)

Meta Options:

ordering: ['-event_date', '-uploaded_at']
verbose_name: "Media Item"
verbose_name_plural: "Media Gallery"
indexes on: media_type, category, is_featured

Model Methods:

get_thumbnail_url(): Return thumbnail for videos or image preview
str(): Return title and media type

SiteSettings Model
Purpose: Dynamic site configuration manageable from admin
Fields:

id: AutoField (Primary Key, only one record exists)
about_overview: TextField (content for About Us overview page)
mission_statement: TextField (NGO mission)
vision_statement: TextField (NGO vision)
achievements_summary: TextField (key achievements)
total_beneficiaries: IntegerField (cumulative count)
total_projects: IntegerField (cumulative count)
established_year: IntegerField (year NGO was founded)
registration_number: CharField (max_length=100, legal registration)
homepage_hero_title: CharField (max_length=200)
homepage_hero_subtitle: CharField (max_length=300)
donation_appeal_text: TextField (text encouraging donations)
volunteer_appeal_text: TextField (text encouraging volunteering)
footer_about_text: TextField (short about text for footer)
meta_description: CharField (max_length=160, for SEO)
meta_keywords: CharField (max_length=300, for SEO)
updated_at: DateTimeField (auto_now)
updated_by: ForeignKey (to User model, last admin who updated)

Meta Options:

verbose_name: "Site Settings"
verbose_name_plural: "Site Settings"

Model Methods:

save(): Override to ensure only one record exists
@classmethod get_settings(): Return the single settings instance
str(): Return "Site Settings"

4.2 Database Relationships
One-to-Many Relationships:

WorkProjects → ProjectGallery (one project has many gallery images)
User → Volunteers (one admin can approve many volunteers)
User → MediaGallery (one admin can upload many media items)
User → SiteSettings (track who last updated settings)

Foreign Key Cascades:

ProjectGallery.project: CASCADE (delete gallery when project deleted)
Volunteers.approved_by: SET_NULL (keep volunteer record if admin deleted)
MediaGallery.uploaded_by: SET_NULL (keep media if admin deleted)

4.3 Database Indexes Strategy
Performance Optimization:

Index frequently queried fields: email, status, dates
Composite indexes for common filter combinations
Unique indexes for transaction references, slugs, volunteer emails
Full-text search indexes for project descriptions (if needed)

4.4 Migration Strategy
Development to Production:

Create all models in development environment
Generate migrations: python manage.py makemigrations
Apply migrations locally: python manage.py migrate
Test all database operations thoroughly
Commit migration files to version control
On cPanel deployment:

Upload project with migration files
Run python manage.py migrate on production database
Database schema automatically created



Data Migration Plan:

Initial deployment: Empty database with schema only
Admin creates first superuser: python manage.py createsuperuser
Admin populates initial data via Django admin interface
Backup strategy: Regular MySQL dumps via cPanel


5. Page-by-Page Functional Specifications
5.1 Home Page (/ or /home)
Purpose
Primary landing page introducing the NGO, showcasing impact, and encouraging action
URL Pattern
Path: '' (root) or 'home/'
View Function: home_view
Template: home.html
URL Name: 'home'
Visual Layout
Hero Section (Full Viewport Height):

Background: Rotating image slider with 2-3 high-quality images
Overlay: Semi-transparent dark gradient for text readability
Content:

NGO logo (top center or as per header)
Main headline: "Shree Brijwasi Jatav Samaj Sewa Samiti"
Subheadline: "Journey of Empowerment and Impact"
Tagline from config
Two CTA buttons:

"Donate Now" (primary button, theme color)
"Become a Volunteer" (secondary button, outline style)




Slider controls: Dots/indicators at bottom, auto-advance every 5 seconds

Introduction Section:

Heading: "Who We Are"
Paragraph: NGO mission and brief introduction (from SiteSettings model)
Statistics cards (4-column grid):

Total Beneficiaries Served
Projects Completed
Active Volunteers
Years of Service


Each card: Icon, number (animated counter), label

Our Impact Section:

Heading: "Our Journey of Empowerment"
Subheading: Brief impact statement
Featured projects carousel:

3 recent projects from WorkProjects model (is_featured=True)
Each project card:

Featured image
Project title
Category badge
Short description (truncated to 150 chars)
"Learn More" link to project detail




Carousel navigation: Left/right arrows

Call to Action Section:

Two-column layout:

Left: "Support Our Mission" with donation appeal text

"Donate Now" button


Right: "Join Our Team" with volunteer appeal text

"Register as Volunteer" button




Background: Light theme color or image

Recent Updates Section:

Heading: "Latest from Our Work"
3 most recent work projects or media items
Grid layout with image, title, date, excerpt
"View All Updates" button linking to Our Work page

Testimonials Section (Optional):

Quotes from beneficiaries or volunteers
Rotating testimonials with photo, name, quote
Adds credibility and emotional connection

Backend Functionality
View Function Logic:
Function: home_view(request)

GET Request Processing:
1. Query SiteSettings.get_settings() for homepage content
2. Query WorkProjects.objects.filter(is_featured=True, is_published=True)[:3]
3. Query aggregate statistics:
   - Total donations: Donations.objects.filter(payment_status='completed').aggregate(Sum('amount'))
   - Total volunteers: Volunteers.objects.filter(is_active=True).count()
   - Total beneficiaries: SiteSettings.total_beneficiaries
   - Total projects: WorkProjects.objects.filter(project_status='completed').count()
4. Load slider images from SLIDER_CONFIG
5. Prepare context dictionary with all data
6. Render 'home.html' with context

POST Request: Not applicable for home page

Return: HttpResponse with rendered template
Context Data Passed to Template:
context = {
    'site_settings': SiteSettings object,
    'slider_images': List of image paths,
    'slider_config': Configuration from config.py,
    'featured_projects': QuerySet of WorkProjects,
    'statistics': {
        'total_donations': Decimal amount,
        'total_volunteers': Integer count,
        'total_beneficiaries': Integer from settings,
        'total_projects': Integer count,
        'years_of_service': Calculated from established_year
    },
    'donation_appeal': Text from settings,
    'volunteer_appeal': Text from settings,
    'recent_updates': Latest 3 projects or media items
}
Frontend Components
Image Slider JavaScript:
Initialize slider on page load
Load images from slider_images array
Set interval from slider_config.SLIDER_INTERVAL
Implement fade transition between slides
Add prev/next button handlers
Add dot indicator click handlers
Pause on hover functionality
Preload all images for smooth transitions
Animated Statistics Counter:
Use Intersection Observer API to trigger when section visible
Animate numbers from 0 to target value over 2 seconds
Use easing function for smooth animation
Format numbers with commas for large values
Lazy Loading:
Implement lazy loading for images below fold
Use Intersection Observer or native loading="lazy"
Reduces initial page load time
Performance Optimization
Target: 3-second page load time
Image Optimization:

Slider images: Max 1920x1080px, WebP format, quality 80%
Project thumbnails: Max 600x400px, WebP format, quality 75%
Lazy load all images except slider
Use srcset for responsive images

Code Optimization:

Minify CSS and JavaScript
Combine CSS files where possible
Defer non-critical JavaScript
Use Django template fragment caching for statistics

Database Optimization:

Use select_related() for foreign key queries
Cache expensive queries (statistics) for 5 minutes
Index all queried fields

Server Optimization:

Enable GZIP compression
Set proper cache headers for static files
Use Django's static file caching

Testing Method:

Use Google PageSpeed Insights
Target: 90+ score on mobile and desktop
Monitor actual load times in production


5.2 About Us - Overview Page (/about/overview)
Purpose
Provide detailed information about NGO's history, mission, vision, and values
URL Pattern
Path: 'about/overview/'
View Function: about_overview_view
Template: about_overview.html
URL Name: 'about_overview'
Visual Layout
Page Header:

Page title: "About Us"
Breadcrumb: Home > About Us > Overview
Subtitle: Brief introduction

Mission & Vision Section:

Two-column layout:

Left: Mission Statement with icon
Right: Vision Statement with icon


Background cards with theme colors

Our Story Section:

Timeline layout (vertical on mobile, horizontal on desktop):

Establishment year and founding story
Key milestones with dates
Major achievements
Growth indicators


Each milestone: Year, title, description, optional image

Our Values Section:

Grid of value cards (2x2 or 3x2):

Integrity
Empowerment
Community Service
Transparency
Inclusivity
Excellence


Each card: Icon, value name, brief description

Registration & Legal Info:

Registration number
Legal status
Certifications (if any)
Transparent operations statement

Our Approach Section:

How the NGO works
Methodology and philosophy
Collaboration approach
Impact measurement

Backend Functionality
View Function Logic:
Function: about_overview_view(request)

GET Request Processing:
1. Query SiteSettings.get_settings()
2. Extract about_overview, mission_statement, vision_statement
3. Calculate years of operation (current year - established_year)
4. Prepare context with all overview content

POST Request: Not applicable

Return: HttpResponse with rendered template
Context Data:
context = {
    'site_settings': SiteSettings object,
    'years_of_operation': Calculated integer,
    'page_title': 'About Us - Overview',
    'meta_description': SEO description
}
Frontend Components
Timeline Animation:
Scroll-triggered animations for timeline items
Fade in elements as user scrolls
Progressive disclosure of content
Value Cards Hover Effects:
Card elevation on hover
Smooth transitions
Icon animation on hover

5.3 About Us - Our Team Page (/about/team)
Purpose
Showcase NGO leadership and team members
URL Pattern
Path: 'about/team/'
View Function: team_view
Template: team.html
URL Name: 'team'
Visual Layout
Page Header:

Page title: "Our Team"
Breadcrumb: Home > About Us > Our Team
Subtitle: "Meet the people driving our mission"

Team Members Grid:

Responsive grid layout (3 columns desktop, 2 tablet, 1 mobile)
Team member cards:

Professional photo (square or circular crop)
Name
Position
Brief bio (expandable on click or full on hover)
Contact email (if public)
Social media links (if available)


Order by display_order field

Leadership Section:

Separate section for key positions:

President
Vice President
Secretary
Treasurer


Larger card format with more detailed bio

Advisory Board Section (if applicable):

Similar grid for advisors
Different styling to distinguish from core team

Backend Functionality
View Function Logic:
Function: team_view(request)

GET Request Processing:
1. Query TeamMembers.objects.filter(is_active=True).order_by('display_order', 'name')
2. Separate leadership positions from general members
3. Prepare context with team data

POST Request: Not applicable

Return: HttpResponse with rendered template
Context Data:
context = {
    'leadership': QuerySet of key positions,
    'team_members': QuerySet of other active members,
    'page_title': 'Our Team',
    'meta_description': SEO description
}
Frontend Components
Modal for Full Bio:
Click on team member opens modal
Display full bio, contact info, social links
Close button and click-outside-to-close
Photo Hover Effects:
Smooth zoom on hover
Overlay with social icons
Grayscale to color transition

5.4 Our Work Page (/our-work)
Purpose
Display all projects and initiatives undertaken by the NGO
URL Pattern
Path: 'our-work/'
View Function: our_work_view
Template: our_work.html
URL Name: 'our_work'
Visual Layout
Page Header:

Page title: "Our Work"
Breadcrumb: Home > Our Work
Subtitle: "Making a difference through action"

Filter/Category Section:

Horizontal filter tabs:

All Projects
Education
Health
Environment
Women Empowerment
Child Welfare
Community Development


Status filter: All, Ongoing, Completed
JavaScript-based filtering (no page reload)

Projects Grid:

Masonry or regular grid layout
Project cards:

Featured image
Category badge
Project title
Short description (truncated)
Status indicator (Ongoing/Completed)
Start date
Beneficiaries count
"View Details" button


Pagination (12 projects per page)

Impact Summary Bar:

Total projects completed
Total beneficiaries reached
Total budget invested
Active ongoing projects

Backend Functionality
View Function Logic:
Function: our_work_view(request)

GET Request Processing:
1. Get filter parameters from request.GET:
   - category (default: all)
   - status (default: all)
   - page number for pagination

2. Build query:
   - Base: WorkProjects.objects.filter(is_published=True)
   - If category specified: .filter(category=category)
   - If status specified: .filter(project_status=status)
   - Order by: -start_date

3. Paginate results (12 per page)

4. Calculate aggregate statistics

5. Prepare context with filtered projects and stats

POST Request: Not applicable

Return: HttpResponse with rendered template
Context Data:
context = {
    'projects': Paginated QuerySet,
    'categories': Choices from model,
    'selected_category': Current filter,
    'selected_status': Current filter,
    'statistics': Aggregate data,
    'page_obj': Pagination object,
    'page_title': 'Our Work',
}
Frontend Components
Filter Functionality:
JavaScript filter without page reload
Show/hide projects based on selected category
Update URL with query parameters
Smooth transitions between filter states
Lazy Loading:
Load initial 12 projects
Infinite scroll or "Load More" button for additional projects
Optimize performance for large project lists
Project Card Hover:
Elevation effect on hover
Display quick stats overlay
Smooth image zoom

5.5 Work Project Detail Page (/our-work/<slug>)
Purpose
Detailed view of a single project with full information and gallery
URL Pattern
Path: 'our-work/<slug:slug>/'
View Function: project_detail_view
Template: project_detail.html
URL Name: 'project_detail'
Visual Layout
Project Header:

Full-width featured image
Overlay with project title, category, status
Breadcrumb: Home > Our Work > Project Title

Project Information Section:

Project details:

Start date, End date (if completed)
Location
Beneficiaries count
Budget (if public)
Partners/collaborators


Status indicator
Social share buttons

Description Section:

Full project description (formatted text)
Problem statement
Solution approach
Implementation details
Outcomes and impact

Photo Gallery Section:

Grid of project images from ProjectGallery model
Lightbox functionality to view full-size images
Image captions
Navigation between images

Related Projects Section:

3 similar projects (same category)
Small cards with image, title, link

CTA Section:

"Support this cause" - link to donation page
"Get involved" - link to volunteer page

Backend Functionality
View Function Logic:
Function: project_detail_view(request, slug)

GET Request Processing:
1. Get project: get_object_or_404(WorkProjects, slug=slug, is_published=True)
2. Increment project.views_count and save
3. Get project gallery images: project.gallery_images.all()
4. Get related projects: WorkProjects.objects.filter(category=project.category).exclude(id=project.id)[:3]
5. Prepare context with project data

POST Request: Not applicable

Return: HttpResponse with rendered template
Context Data:
context = {
    'project': WorkProjects object,
    'gallery_images': QuerySet of ProjectGallery,
    'related_projects': QuerySet of similar projects,
    'page_title': project.title,
    'meta_description': project.short_description,
}
Frontend Components
Lightbox Gallery:
Click image opens full-screen lightbox
Navigation arrows between images
Close button and ESC key support
Display image caption
Zoom in/out functionality
Social Share:
Share buttons for Facebook, Twitter, WhatsApp, Email
Copy link to clipboard functionality
Dynamic share text with project title

5.6 Donation Page (/donate
Purpose
Enable online donations through UPI payment system
URL Pattern
Path: 'donate/'
View Function: donate_view
Template: donate.html
URL Name: 'donate'
Visual Layout
Page Header:

Page title: "Support Our Mission"
Breadcrumb: Home > Donate
Motivational subtitle about impact of donations

Donation Impact Section:

Visual representation of how donations help:

₹500: Education materials for 1 child
₹1000: Healthcare support for 1 family
₹5000: Community program for 1 month
Custom amount option



Donation Form:

Amount selection:

Pre-defined amounts (₹500, ₹1000, ₹2000, ₹5000, ₹10000)
Custom amount input


Donor information:

Full name (required)
Email address (required, for receipt)
Phone number (optional)
Donation purpose (optional dropdown or text)
Make donation anonymous (checkbox)


UPI Payment Selection:

Radio buttons or cards for:

Google Pay
PhonePe
Paytm
BHIM
Other UPI App


Visual logos for each app


Terms acceptance checkbox
"Proceed to Payment" button (theme color, prominent)

How It Works Section:

Step-by-step guide:

Enter amount and details
Select UPI app
Complete payment in app
Receive confirmation email


Security badges (SSL, secure payment)

Recent Donors Section:

List of recent non-anonymous donors (first name + last initial)
Amount and date
"Thank you" message
Privacy note

Tax Benefits Section:

Information about 80G tax exemption (if applicable)
How to claim tax benefits
Receipt information

Backend Functionality
View Function Logic:
Function: donate_view(request)

GET Request Processing:
1. Load recent donations: Donations.objects.filter(payment_status='completed', is_anonymous=False).order_by('-completed_at')[:10]
2. Load payment configuration from PAYMENT_CONFIG
3. Render form with donation options

POST Request Processing:
1. Validate form data:
   - Amount must be >= MINIMUM_DONATION from config
   - Name and email are required
   - UPI app selection required

2. Create donation record:
   - Generate unique transaction_reference
   - Set payment_status = 'pending'
   - Save donor details
   - Set created_at timestamp

3. Build UPI deep link:
   - Format: upi://pay?pa=VPA&pn=PAYEE_NAME&am=AMOUNT&tn=REFERENCE&cu=INR
   - pa: UPI VPA from config
   - pn: Payee name from config
   - am: Donation amount
   - tn: Transaction reference
   - cu: Currency (INR)

4. Generate app-specific deep links:
   - Google Pay: tez://upi/pay?...
   - PhonePe: phonepe://pay?...
   - Paytm: paytmmp://pay?...
   - BHIM: bhim://pay?...

5. Return JSON response or redirect:
   - If AJAX: Return JSON with deep link
   - If regular form: Redirect to payment confirmation page with link
   - Store deep link in session for callback

6. Handle errors:
   - Validation errors: Re-render form with error messages
   - Database errors: Log and show user-friendly error

Return: HttpResponse with rendered form or redirect to payment
Context Data (GET):
context = {
    'recent_donors': QuerySet of recent donations,
    'minimum_donation': From PAYMENT_CONFIG,
    'suggested_amounts': [500, 1000, 2000, 5000, 10000],
    'upi_apps': List of supported apps with logos,
    'upi_vpa': From PAYMENT_CONFIG,
    'page_title': 'Donate Now',
}
Payment Callback Handling:
Separate view for payment confirmation:
Function: payment_callback_view(request, transaction_reference)

1. Get donation record by transaction_reference
2. Show payment confirmation page with:
   - Transaction details
   - Payment status check instructions
   - Verification form for admin

3. Admin verification:
   - Manual process: Admin receives UPI notification
   - Admin logs into Django admin
   - Updates payment_status to 'completed'
   - Enters upi_transaction_id from payment app
   - System sends receipt email automatically

Alternative: Auto-verification via payment gateway webhook (if available)
Frontend Components
Amount Selection:
Click pre-defined amount buttons to populate input
Highlight selected amount
Allow custom amount entry
Validate minimum amount in real-time
UPI App Selection:
Visual cards for each UPI app
Highlight selected app
Show app logo and name
Detect installed apps (mobile only) and highlight available
Form Validation:
Real-time validation on blur:
- Name: Minimum 2 characters
- Email: Valid email format
- Amount: Minimum and numeric check
- UPI app: Selection required
Show error messages below fields
Disable submit until all valid
Payment Redirect:
On form submit:
1. Show loading spinner
2. Submit form via AJAX
3. Receive deep link from backend
4. Redirect user to UPI app
5. Show instructions for completing payment
6. Provide "I have completed payment" button
7. Redirect to thank you page with pending status
Thank You Page:
Display after payment initiation:
- Thank you message
- Transaction reference number
- Payment verification instructions
- "Your receipt will be emailed once verified"
- Estimated verification time
- Link back to home or other pages
Email Notifications
Donor Confirmation Email:
Trigger: Immediately after donation initiated
Subject: "Thank you for your donation - Pending Confirmation"
Content:
- Thank you message
- Transaction reference
- Pending status
- Instructions to wait for verification
- Contact info for queries
Donor Receipt Email:
Trigger: When admin marks payment as completed
Subject: "Donation Receipt - Shree Brijwasi Jatav Samaj Sewa Samiti"
Content:
- Formal receipt header with NGO details
- Donor name and details
- Amount donated
- Transaction ID
- Date and time
- Purpose of donation
- Tax benefit information (if applicable)
- Thank you note and impact message
- PDF attachment with formatted receipt
Admin Notification Email:
Trigger: Immediately after donation initiated
Subject: "New Donation Pending Verification"
Content:
- Donor details
- Amount
- Transaction reference
- Link to admin panel for verification
- Reminder to verify within 24 hours
Security Measures
Payment Security:

No payment credentials stored
All transactions through secure UPI protocol
SSL certificate for entire site
CSRF tokens on all forms
Rate limiting to prevent spam

Data Protection:

Donor information encrypted in database
PCI DSS compliance for any card data (if added)
Privacy policy clearly stated
Option for anonymous donations


5.7 Media Page (/media)
Purpose
Gallery of photos and videos from NGO events and activities
URL Pattern
Path: 'media/'
View Function: media_view
Template: media.html
URL Name: 'media'
Visual Layout
Page Header:

Page title: "Media Gallery"
Breadcrumb: Home > Media
Subtitle: "Moments from our journey"

Filter Section:

Category tabs:

All
Events
Activities
Workshops
Achievements


Media type toggle:

All
Photos
Videos



Media Grid:

Masonry grid layout for photos
Mixed photo and video thumbnails
Each item:

Thumbnail image (or video preview)
Title overlay on hover
Play icon for videos
Date badge
Category badge


Click opens lightbox/modal

Lightbox View:

Full-size image or video player
Caption and date
Navigation arrows between items
Close button
Share buttons
Download option (if enabled)

Pagination:

Load more button or infinite scroll
24 items per page

Backend Functionality
View Function Logic:
Function: media_view(request)

GET Request Processing:
1. Get filter parameters:
   - category (default: all)
   - media_type (default: all)
   - page number

2. Build query:
   - Base: MediaGallery.objects.all()
   - If category: .filter(category=category)
   - If media_type: .filter(media_type=media_type)
   - Order by: -event_date, -uploaded_at

3. Paginate results (24 per page)

4. Prepare context with media items

POST Request: Not applicable (unless adding upload feature for logged-in users)

Return: HttpResponse with rendered template
Context Data:
context = {
    'media_items': Paginated QuerySet,
    'categories': Choices from model,
    'selected_category': Current filter,
    'selected_media_type': Current filter,
    'page_obj': Pagination object,
    'page_title': 'Media Gallery',
}
Frontend Components
Masonry Grid:
Use Masonry.js or CSS Grid for layout
Images of varying heights
Responsive columns (4 desktop, 3 tablet, 2 mobile)
Smooth loading animations
Lightbox:
Full-screen overlay
Image display with zoom capability
Video embedded player (YouTube/Vimeo iframe)
Keyboard navigation (arrows, ESC)
Swipe navigation on mobile
Lazy Loading:
Load images as user scrolls
Placeholder blur-up effect
Optimize for many images
IntersectionObserver API
Filter Animation:
Smooth fade transitions when filtering
Reorganize grid without jarring layout shifts
Update URL parameters without reload

5.8 Contact Page (/contact)
Purpose
Provide contact information and submission form for inquiries
URL Pattern
Path: 'contact/'
View Function: contact_view
Template: contact.html
URL Name: 'contact'
Visual Layout
Page Header:

Page title: "Contact Us"
Breadcrumb: Home > Contact
Subtitle: "We'd love to hear from you"

Two-Column Layout:
Left Column - Contact Form:

Form fields:

Name (required)
Email (required)
Phone (optional)
Subject (required)
Message (required, textarea)


reCAPTCHA (optional, for spam prevention)
"Send Message" button

Right Column - Contact Information:

Office address with map icon
Phone number with phone icon
Email address with email icon
Office hours
Social media links with icons

Map Section:

Embedded Google Maps showing office location
Full-width below two columns
Interactive map with marker

FAQ Section (Optional):

Common questions answered
Reduces form submissions for simple queries

Backend Functionality
View Function Logic:
Function: contact_view(request)

GET Request Processing:
1. Load contact information from SITE_CONFIG
2. Render empty contact form

POST Request Processing:
1. Validate form data:
   - Name: Required, min 2 characters
   - Email: Required, valid format
   - Phone: Optional, valid format if provided
   - Subject: Required, max 300 characters
   - Message: Required, min 10 characters

2. Verify reCAPTCHA if enabled:
   - Send verification request to Google
   - Validate response token
   - Reject if fails

3. Create contact submission:
   - Save to ContactSubmissions model
   - Capture IP address for spam tracking
   - Set is_read = False

4. Send emails:
   - Auto-reply to user: Acknowledge receipt
   - Notification to admin: Alert about new submission

5. Success response:
   - Set success message
   - Redirect to same page or thank you page
   - Clear form

6. Error handling:
   - Validation errors: Re-render with messages
   - Email errors: Log but still save submission
   - Database errors: User-friendly error message

Return: HttpResponse with form or redirect
Context Data (GET):
context = {
    'contact_info': From SITE_CONFIG,
    'map_embed_url': Google Maps embed URL,
    'page_title': 'Contact Us',
}
Frontend Components
Form Validation:
Real-time validation on field blur
Email format check
Phone format check (India: 10 digits)
Message length counter
Disable submit until all required fields valid
Map Integration:
Google Maps Embed API
Centered on office location
Custom marker with NGO logo
Info window with address
Responsive embed sizing
Success Message:
Display toast notification on successful submission
Auto-hide after 5 seconds
Green checkmark icon
Email Templates
Auto-Reply to User:
Subject: "We received your message - Shree Brijwasi Jatav Samaj Sewa Samiti"
Content:
- Thank you for contacting us
- Confirmation of message received
- Expected response time (e.g., within 48 hours)
- Copy of their message for reference
- Contact info for urgent matters
Admin Notification:
Subject: "New Contact Form Submission"
Content:
- Sender name and email
- Subject and message
- Submission timestamp
- Link to admin panel to view/respond
- Quick reply option
Spam Prevention
Measures:

reCAPTCHA v3 (invisible, scores requests)
Rate limiting: Max 3 submissions per IP per hour
Honeypot field (hidden field that bots fill)
Email domain validation
Message content filters for spam keywords
Admin can mark submissions as spam


5.9 Volunteer Registration Page (/volunteer)
Purpose
Allow interested individuals to register as volunteers
URL Pattern
Path: 'volunteer/'
View Function: volunteer_view
Template: volunteer.html
URL Name: 'volunteer'
Visual Layout
Page Header:

Page title: "Become a Volunteer"
Breadcrumb: Home > Volunteer
Subtitle: "Join our mission to empower communities"

Why Volunteer Section:

Benefits of volunteering with the organization
Impact volunteers make
Testimonials from current volunteers
Photo of volunteers in action

Volunteer Registration Form:

Personal Information:

Full Name (required)
Email (required)
Phone (required)
Age (optional)
Address (optional)


Volunteer Preferences:

Skills/Expertise (required, textarea)
Preferred area of work (dropdown):

Education
Health
Environment
Community Development
Administration


Availability (dropdown):

Weekdays
Weekends
Flexible
Specific days (with day selector)




Experience:

Previous volunteer experience (optional, textarea)


Additional Information:

Why you want to volunteer (optional, textarea)
Emergency contact name and phone (optional)
Subscribe to newsletter (checkbox, checked by default)


Terms and Conditions:

Accept volunteer agreement (checkbox, required)
Privacy policy acceptance


"Submit Application" button

Volunteer Opportunities Section:

Current volunteer needs
Upcoming events needing volunteers
Special skill requirements

FAQ Section:

Common questions about volunteering
Time commitment expectations
Training provided
Volunteer policies

Backend Functionality
View Function Logic:
Function: volunteer_view(request)

GET Request Processing:
1. Load volunteer opportunities (if model exists)
2. Render registration form

POST Request Processing:
1. Validate form data:
   - Name, email, phone: Required
   - Email: Valid format and unique (not already registered)
   - Phone: Valid format
   - Skills: Required, min 20 characters
   - Preferred area and availability: Required
   - Terms acceptance: Required

2. Check for duplicate registration:
   - Query existing volunteers by email
   - If exists with status='pending' or 'approved': Show error
   - If exists with status='inactive': Allow re-registration

3. Create volunteer record:
   - Save all form data to Volunteers model
   - Set status = 'pending'
   - Set registration_date = now()

4. Send confirmation emails:
   - Welcome email to volunteer
   - Notification email to admin

5. Success response:
   - Redirect to thank you page
   - Display success message
   - Clear form data

6. Error handling:
   - Validation errors: Re-render form with error messages
   - Duplicate email: Specific error message
   - Database errors: Generic error message
   - Email errors: Log but continue (volunteer still registered)

Return: HttpResponse with form or redirect
Context Data (GET):
context = {
    'volunteer_appeal': From SITE_CONFIG,
    'current_opportunities': List of current needs,
    'area_choices': From Volunteers model,
    'availability_choices': From Volunteers model,
    'page_title': 'Volunteer Registration',
}
Frontend Components
Multi-Step Form (Optional Enhancement):
Step 1: Personal Information
Step 2: Volunteer Preferences
Step 3: Experience and Motivation
Step 4: Review and Submit
Progress indicator showing current step
Next/Previous buttons
Save progress to localStorage
Form Validation:
Real-time validation on blur
Email uniqueness check (AJAX to backend)
Phone format validation (India format)
Skills word count (minimum required)
Disable submit until all required fields valid
Visual feedback for valid/invalid fields
Skills Input Enhancement:
Auto-suggest common skills as user types
Tagging interface for multiple skills
Character counter for textarea
Availability Selector:
If "Specific days" selected:
- Show day of week checkboxes
- Time preference selectors
Validate at least one day selected
Email Notifications
Welcome Email to Volunteer:
Subject: "Thank you for volunteering - Shree Brijwasi Jatav Samaj Sewa Samiti"
Content:
- Warm welcome message
- Confirmation of registration received
- What happens next (review process)
- Expected timeline for response
- Contact person for questions
- Link to volunteer resources (if available)
Admin Notification:
Subject: "New Volunteer Registration - [Name]"
Content:
- Volunteer name and contact details
- Skills and preferred area
- Availability
- Link to admin panel to review application
- Quick approve/reject buttons
Approval Email (sent when admin approves):
Subject: "Your volunteer application has been approved!"
Content:
- Congratulations message
- Next steps and onboarding information
- Orientation session details (if applicable)
- Volunteer coordinator contact
- Welcome package information
Admin Workflow
Admin Panel for Volunteer Management:
List view of all volunteer applications:
- Filter by status (pending, approved, active, inactive)
- Search by name, email, skills
- Sortable columns
- Bulk actions (approve, reject)

Detail view for each volunteer:
- All submitted information
- Application date
- Status change buttons (Approve, Reject, Deactivate)
- Notes field for admin comments
- Contact volunteer button (send email)
- Activity log (when registered, approved, last active)
Approval Process:
1. Admin reviews application
2. Clicks "Approve" button
3. System:
   - Updates status to 'approved'
   - Sets approved_date
   - Records approved_by (current admin user)
   - Sends approval email to volunteer
   - Sends notification to volunteer coordinator

5.10 Thank You / Success Pages
Purpose
Acknowledge user actions (donation, volunteer registration, contact)
URL Patterns
Path: 'thank-you/donation/'
Path: 'thank-you/volunteer/'
Path: 'thank-you/contact/'
View Functions: Individual views or single view with parameter
Templates: Dedicated or single template with conditionals
Visual Layout
Common Elements:

Large checkmark or success icon
"Thank You" heading
Personalized message based on action
Next steps information
Call to action buttons
Link back to home or other pages

Donation Thank You:

Message: "Thank you for your generous donation!"
Transaction reference number (prominently displayed)
Payment verification status
Expected timeline for receipt email
Impact statement (how donation helps)
Share buttons to spread the word
"Donate Again" button
"Become a Volunteer" button

Volunteer Thank You:

Message: "Thank you for registering as a volunteer!"
Application confirmation
What happens next (review process, timeline)
Volunteer resources links
"Share with Friends" buttons
"Return Home" button

Contact Thank You:

Message: "Thank you for contacting us!"
Confirmation of message received
Expected response time
Alternative contact methods
FAQ link
"Return Home" button

Backend Functionality
View Functions:
Function: donation_thank_you_view(request, transaction_reference)
- Verify transaction_reference exists
- Get donation details
- Render thank you page with transaction info

Function: volunteer_thank_you_view(request)
- Display generic success message
- No sensitive data needed

Function: contact_thank_you_view(request)
- Display generic success message
- Offer additional resources

6. File Structure
6.1 Project Directory Organization
ngo_website/                          # Django project root
│
├── manage.py                          # Django management script
│
├── config/                            # Configuration directory
│   ├── __init__.py
│   ├── config.py                      # Development configuration
│   └── config_production.py           # Production (cPanel) configuration
│
├── ngo_site/                          # Django project settings directory
│   ├── __init__.py
│   ├── settings.py                    # Django settings (imports config)
│   ├── urls.py                        # Main URL configuration
│   ├── wsgi.py                        # WSGI entry point for deployment
│   └── asgi.py                        # ASGI entry point (if needed)
│
├── main_app/                          # Main Django application
│   ├── __init__.py
│   ├── admin.py                       # Django admin customization
│   ├── apps.py                        # App configuration
│   ├── models.py                      # All database models
│   ├── views.py                       # All view functions
│   ├── forms.py                       # Django form classes
│   ├── urls.py                        # App-specific URL patterns
│   ├── context_processors.py         # Global template context
│   ├── utils.py                       # Utility functions
│   ├── validators.py                  # Custom validators
│   │
│   ├── migrations/                    # Database migrations
│   │   ├── __init__.py
│   │   ├── 0001_initial.py
│   │   └── ...
│   │
│   └── management/                    # Custom management commands
│       ├── __init__.py
│       └── commands/
│           ├── __init__.py
│           └── create_sample_data.py  # Populate test data
│
├── templates/                         # Template directory
│   ├── base.html                      # Master template
│   │
│   ├── includes/                      # Reusable components
│   │   ├── header.html
│   │   ├── navigation.html
│   │   ├── footer.html
│   │   ├── donation_card.html
│   │   ├── team_card.html
│   │   └── project_card.html
│   │
│   ├── pages/                         # Page templates
│   │   ├── home.html
│   │   ├── about_overview.html
│   │   ├── team.html
│   │   ├── our_work.html
│   │   ├── project_detail.html
│   │   ├── donate.html
│   │   ├── media.html
│   │   ├── contact.html
│   │   └── volunteer.html
│   │
│   ├── thank_you/                     # Success pages
│   │   ├── donation.html
│   │   ├── volunteer.html
│   │   └── contact.html
│   │
│   ├── emails/                        # Email templates
│   │   ├── donation_confirmation.html
│   │   ├── donation_receipt.html
│   │   ├── volunteer_welcome.html
│   │   ├── volunteer_approved.html
│   │   ├── contact_auto_reply.html
│   │   └── admin_notification.html
│   │
│   └── errors/                        # Error pages
│       ├── 404.html
│       ├── 500.html
│       └── 403.html
│
├── static/                            # Static files directory
│   ├── css/                           # Stylesheets
│   │   ├── styles.css                 # Main stylesheet with theme
│   │   ├── responsive.css             # Media queries
│   │   └── admin_custom.css           # Admin panel customization
│   │
│   ├── js/                            # JavaScript files
│   │   ├── main.js                    # Main JavaScript
│   │   ├── slider.js                  # Image slider logic
│   │   ├── forms.js                   # Form validation
│   │   ├── donation.js                # Donation page logic
│   │   ├── gallery.js                 # Media gallery lightbox
│   │   └── utils.js                   # Utility functions
│   │
│   ├── images/                        # Image assets
│   │   ├── logo.png                   # NGO logo
│   │   ├── favicon.ico                # Favicon
│   │   │
│   │   ├── slider/                    # Homepage slider images
│   │   │   ├── slide1.webp
│   │   │   ├── slide2.webp
│   │   │   └── slide3.webp
│   │   │
│   │   ├── icons/                     # UI icons
│   │   │   ├── education.svg
│   │   │   ├── health.svg
│   │   │   ├── environment.svg
│   │   │   └── ...
│   │   │
│   │   ├── upi/                       # UPI app logos
│   │   │   ├── googlepay.png
│   │   │   ├── phonepe.png
│   │   │   ├── paytm.png
│   │   │   └── bhim.png
│   │   │
│   │   └── placeholders/              # Placeholder images
│   │       ├── team_placeholder.jpg
│   │       └── project_placeholder.jpg
│   │
│   ├── fonts/                         # Custom fonts (if any)
│   │   └── ...
│   │
│   └── vendor/                        # Third-party libraries
│       ├── bootstrap/
│       ├── jquery/
│       └── ...
│
├── media/                             # User-uploaded files (not in repo)
│   ├── team_photos/
│   ├── work_projects/
│   ├── project_gallery/
│   ├── media_gallery/
│   └── donation_receipts/             # Generated PDF receipts
│
├── logs/                              # Application logs (not in repo)
│   ├── django.log
│   ├── error.log
│   └── payment.log
│
├── requirements.txt                   # Python dependencies
├── .env.example                       # Environment variables template
├── .gitignore                         # Git ignore file
├── README.md                          # Project documentation
│
└── deployment/                        # Deployment scripts
    ├── setup_cpanel.sh               # cPanel setup script
    ├── .htaccess                     # Apache configuration for cPanel
    ├── passenger_wsgi.py             # Passenger WSGI entry point
    └── backup.sh                      # Database backup script
6.2 Key File Purposes
Configuration Files:

config/config.py: Development environment settings (localhost, XAMPP MySQL)
config/config_production.py: Production settings (cPanel database, domain)
.env.example: Template for environment variables (copy to .env locally)

Core Django Files:

ngo_site/settings.py: Imports appropriate config, defines Django settings
ngo_site/urls.py: Routes URLs to views
main_app/models.py: All database model definitions in single file
main_app/views.py: All view functions in single file
main_app/forms.py: Django form classes for validation
main_app/admin.py: Admin panel customization

Template Files:

base.html: Master template with header, footer, common structure
pages/*.html: Individual page templates extending base
includes/*.html: Reusable component templates
emails/*.html: HTML email templates

Static Files:

static/css/styles.css: Main stylesheet with theme colors
static/js/main.js: Main JavaScript with all interactive features
static/images/: All image assets organized by purpose

Media Files:

media/: User-uploaded content (gitignored, created on server)

Deployment Files:

requirements.txt: Python package dependencies
deployment/.htaccess: Apache rewrite rules for cPanel
deployment/passenger_wsgi.py: Entry point for Passenger


7. Deployment Workflow
7.1 Local Development (XAMPP)
Initial Setup
Step 1: Install Prerequisites
- Install XAMPP (Apache + MySQL)
- Install Python 3.9+ (standalone, not XAMPP's Python)
- Install pip
- Install virtualenv: pip install virtualenv
Step 2: Create Project Environment
1. Create project directory: mkdir ngo_website
2. Navigate to directory: cd ngo_website
3. Create virtual environment: virtualenv venv
4. Activate virtual environment:
   - Windows: venv\Scripts\activate
   - Mac/Linux: source venv/bin/activate
5. Install Django: pip install django
6. Install other dependencies:
   pip install mysqlclient
   pip install pillow
   pip install python-decouple
   (see requirements.txt for full list)
Step 3: Start XAMPP MySQL
1. Open XAMPP Control Panel
2. Start MySQL service
3. Open phpMyAdmin (http://localhost/phpmyadmin)
4. Create database: ngo_website_db
5. Create database user (or use root for development)
Step 4: Configure Django Project
1. Create Django project: django-admin startproject ngo_site .
2. Create Django app: python manage.py startapp main_app
3. Add main_app to INSTALLED_APPS in settings.py
4. Configure config/config.py:
   DATABASE_CONFIG = {
       'ENGINE': 'django.db.backends.mysql',
       'NAME': 'ngo_website_db',
       'USER': 'root',
       'PASSWORD': '',  # or XAMPP MySQL password
       'HOST': '127.0.0.1',
       'PORT': '3306',
   }
5. Update settings.py to import config
Step 5: Create Database Schema
1. Define all models in main_app/models.py
2. Create migrations: python manage.py makemigrations
3. Apply migrations: python manage.py migrate
4. Create superuser: python manage.py createsuperuser
   - Enter username, email, password
Step 6: Run Development Server
1. Collect static files: python manage.py collectstatic
2. Run server: python manage.py runserver
3. Access site: http://127.0.0.1:8000
4. Access admin: http://127.0.0.1:8000/admin
Development Workflow
Daily Development Process:
1. Activate virtual environment
2. Start XAMPP MySQL service
3. Run Django development server
4. Edit code (views, templates, static files)
5. Refresh browser to see changes
6. Test functionality
7. Commit changes to Git
Testing Checklist:
- Test all forms (validation, submission, error handling)
- Test database operations (create, read, update, delete)
- Test email sending (use Django console backend for dev)
- Test file uploads (images for team, projects, media)
- Test responsive design (mobile, tablet, desktop)
- Test all links and navigation
- Test payment flow (UPI deep link generation)
- Check page load times (especially homepage)
7.2 Production Deployment (cPanel)
Pre-Deployment Preparation
Step 1: Prepare Production Configuration
1. Create config/config_production.py
2. Update database credentials (get from cPanel):
   DATABASE_CONFIG = {
       'ENGINE': 'django.db.backends.mysql',
       'NAME': 'cpanel_username_ngo_db',  # cPanel format
       'USER': 'cpanel_username_ngo_user',
       'PASSWORD': 'strong_password_here',
       'HOST': 'localhost',  # or server hostname
       'PORT': '3306',
   }
3. Update ALLOWED_HOSTS with domain name
4. Set DEBUG = False
5. Configure static and media file paths for cPanel
Step 2: Prepare Static Files
1. Run collectstatic: python manage.py collectstatic
2. Verify all static files in staticfiles/ directory
3. Minify CSS and JavaScript (optional but recommended)
4. Optimize images (compress, convert to WebP)
Step 3: Generate Requirements File
1. Freeze dependencies: pip freeze > requirements.txt
2. Verify all required packages listed
3. Remove any development-only packages
Step 4: Test Locally with Production Settings
1. Temporarily use config_production.py locally
2. Set DEBUG = False
3. Test with production database settings (if possible)
4. Ensure no errors occur
5. Revert to development config
cPanel Deployment Steps
Step 1: Access cPanel
1. Log into cPanel (typically: yourdomain.com/cpanel)
2. Navigate to File Manager
3. Go to public_html or create subdirectory for app
Step 2: Upload Project Files
Method A: File Manager Upload
1. Zip entire project directory (exclude venv, media, logs, __pycache__)
2. Upload zip via cPanel File Manager
3. Extract zip file

Method B: FTP Upload
1. Use FileZilla or similar FTP client
2. Connect using cPanel FTP credentials
3. Upload all files maintaining directory structure

Method C: Git Deployment (if available)
1. Initialize Git repo in cPanel
2. Add remote repository
3. Pull code from remote
Step 3: Set Up Python Environment
1. In cPanel, go to "Setup Python App" or "Application Manager"
2. Create new Python application:
   - Python version: 3.9 or higher
   - Application root: /home/username/ngo_website
   - Application URL: yourdomain.com
3. Enter virtual environment
4. Install dependencies:
   pip install -r requirements.txt
Step 4: Configure Database
1. In cPanel MySQL Databases:
   - Create database: username_ngo_db
   - Create user: username_ngo_user
   - Set strong password
   - Add user to database with ALL PRIVILEGES
2. Note down database credentials
3. Update config/config_production.py with these credentials
Step 5: Update Configuration
1. Edit config/config_production.py on server:
   - Database credentials
   - ALLOWED_HOSTS = ['yourdomain.com', 'www.yourdomain.com']
   - STATIC_ROOT and MEDIA_ROOT paths
   - Email settings (SMTP server)
2. Verify settings.py imports production config based on environment
Step 6: Run Migrations
1. Access terminal/SSH (if available) or use cPanel Python app terminal
2. Navigate to project directory
3. Run: python manage.py migrate
4. Database tables created automatically
5. Create superuser: python manage.py createsuperuser
Step 7: Collect Static Files
1. Run: python manage.py collectstatic --noinput
2. Static files copied to STATIC_ROOT
3. Verify files accessible at yourdomain.com/static/
Step 8: Configure WSGI
1. cPanel creates passenger_wsgi.py automatically
2. Verify it points to correct application:
   from ngo_site.wsgi import application
3. If custom configuration needed, edit deployment/passenger_wsgi.py
4. Set correct paths for virtual environment
Step 9: Set File Permissions
1. media/ directory: 755 (writable for uploads)
2. logs/ directory: 755 (writable for logging)
3. Python files: 644 (read-only)
4. Directories: 755
5. Sensitive files (config): 600 (owner read/write only)
Step 10: Configure .htaccess (if needed)
Create or edit .htaccess for:
- Force HTTPS: Redirect HTTP to HTTPS
- WWW redirect: yourdomain.com to www.yourdomain.com (or vice versa)
- Passenger configuration
- Static file serving optimization

Example .htaccess:
RewriteEngine On
RewriteCond %{HTTPS} off
RewriteRule ^(.*)$ https://%{HTTP_HOST}%{REQUEST_URI} [L,R=301]
Step 11: Restart Application
1. In cPanel Python App Manager, click "Restart"
2. Or create/touch tmp/restart.txt in application root
3. Verify site loads at yourdomain.com
Step 12: Post-Deployment Verification
1. Visit yourdomain.com
2. Check all pages load correctly
3. Test forms (contact, volunteer, donation)
4. Verify static files (CSS, JS, images) load
5. Test image uploads via admin panel
6. Send test emails (donation, contact confirmations)
7. Test UPI payment flow
8. Check error logs for any issues
9. Test on mobile devices
10. Run Google PageSpeed Insights
Troubleshooting Common Issues
Issue: Database Connection Error
Solution:
- Verify database credentials in config_production.py
- Check MySQL user has correct privileges
- Ensure database host is correct (usually 'localhost')
- Test connection via cPanel phpMyAdmin
Issue: Static Files Not Loading
Solution:
- Run collectstatic again
- Verify STATIC_ROOT path is correct
- Check .htaccess allows access to static/
- Ensure file permissions are correct (755 for directories, 644 for files)
Issue: 500 Internal Server Error
Solution:
- Set DEBUG = True temporarily to see error details
- Check error logs in cPanel or logs/ directory
- Verify all dependencies installed (pip install -r requirements.txt)
- Check WSGI configuration
- Ensure SECRET_KEY is set
Issue: Images Not Uploading
Solution:
- Verify media/ directory exists and is writable (755)
- Check MEDIA_ROOT and MEDIA_URL in settings
- Ensure PIL/Pillow installed correctly
- Check file size limits in cPanel
Issue: Emails Not Sending
Solution:
- Verify SMTP settings in config_production.py
- Test SMTP credentials separately
- Check spam folder for test emails
- Enable less secure apps if using Gmail
- Consider using SendGrid or similar service
7.3 Updating Deployed Site
Process for Code Updates:
1. Make changes in local development environment
2. Test thoroughly
3. Commit to Git
4. Upload changed files to cPanel via FTP or Git pull
5. If models changed:
   - Create and apply new migrations
   - python manage.py makemigrations
   - python manage.py migrate
6. If static files changed:
   - python manage.py collectstatic --noinput
7. Restart application
8. Verify changes in production
Process for Content Updates:
1. Admin logs into Django admin panel (yourdomain.com/admin)
2. Add/edit/delete content:
   - Team members
   - Work projects
   - Media gallery items
   - Site settings
3. Changes reflected immediately
4. No code deployment needed

8. Security Implementation
8.1 Django Security Best Practices
Settings Configuration:
- SECRET_KEY: Strong, random, never committed to version control
- DEBUG = False in production
- ALLOWED_HOSTS: Specific domain names only
- SECURE_SSL_REDIRECT = True (force HTTPS)
- SESSION_COOKIE_SECURE = True
- CSRF_COOKIE_SECURE = True
- SECURE_BROWSER_XSS_FILTER = True
- X_FRAME_OPTIONS = 'DENY'
- SECURE_CONTENT_TYPE_NOSNIFF = True
CSRF Protection:
- Enabled by default in Django
- Include {% csrf_token %} in all forms
- Verify CSRF middleware in MIDDLEWARE setting
- AJAX requests include CSRF token in headers
SQL Injection Prevention:
- Always use Django ORM (never raw SQL unless necessary)
- If raw SQL needed, use parameterized queries
- Never interpolate user input into SQL strings
XSS Prevention:
- Django templates auto-escape variables by default
- Use |safe filter only for trusted content
- Sanitize user input before storing
- Content Security Policy headers
8.2 Payment Security
UPI Transaction Security:
- Generate unique transaction references
- Validate all amounts server-side
- Never trust client-side data
- Log all payment attempts with timestamps
- Rate limit payment requests (prevent spam)
- Verify payment status before marking complete
Data Protection:
- Store minimal payment information
- Never store UPI pins or passwords
- Encrypt sensitive donor data
- Hash IP addresses for privacy
- Regular security audits of payment flow
8.3 File Upload Security
Image Upload Restrictions:
- Validate file types (check extension and MIME type)
- Limit file sizes (max 5MB for images, 20MB for videos)
- Rename uploaded files (don't use original names)
- Store outside web root if possible
- Scan for malware (if budget allows)
Upload Validation:
def validate_image(file):
    # Check file extension
    valid_extensions = ['jpg', 'jpeg', 'png', 'webp', 'gif']
    ext = file.name.split('.')[-1].lower()
    if ext not in valid_extensions:
        raise ValidationError('Invalid file type')
    
    # Check file size
    if file.size > 5 * 1024 * 1024:  # 5MB
        raise ValidationError('File too large')
    
    # Check actual image content (prevents fake extensions)
    try:
        from PIL import Image
        img = Image.open(file)
        img.verify()
    except:
        raise ValidationError('Invalid image file')
8.4 User Authentication
Admin Access:
- Strong password requirements
- Two-factor authentication (optional but recommended)
- Account lockout after failed attempts
- Session timeout after inactivity
- Audit log of admin actions
Password Policy:
- Minimum 8 characters
- Mix of uppercase, lowercase, numbers, symbols
- No common passwords
- Different from username
- Regular password rotation
8.5 Spam and Abuse Prevention
Contact Form Protection:
- reCAPTCHA v3 integration
- Rate limiting: 3 submissions per IP per hour
- Honeypot field (hidden field bots fill)
- Email domain validation
- Keyword filtering for spam content
Volunteer Registration Protection:
- Email verification (send confirmation link)
- Rate limiting on registration
- Admin approval before activation
- Duplicate email prevention
Donation Form Protection:
- Minimum donation amount validation
- Maximum donation amount (flag for review if exceeded)
- Rate limiting on donation attempts
- IP tracking and blocking for suspicious activity
8.6 Data Privacy
GDPR Compliance (if applicable):
- Privacy policy page clearly stating data usage
- Cookie consent banner
- Data retention policies
- Right to deletion (users can request data removal)
- Data portability (export user data)
- Secure data storage and transmission
Data Minimization:
- Collect only necessary information
- Don't require optional fields
- Anonymous donation option
- Clear explanation of why data is collected

9. Performance Optimization
9.1 Homepage Load Time Target: ≤3 Seconds
Image Optimization:
Slider Images:
- Maximum resolution: 1920x1080px
- Format: WebP with JPEG fallback
- Compression: 80% quality
- File size target: <200KB each
- Lazy load images below fold
- Preload first slider image

Thumbnails and Icons:
- Maximum resolution: 600x400px for project cards
- Format: WebP with fallback
- Compression: 75% quality
- Use SVG for icons
CSS Optimization:
- Minify CSS (remove whitespace, comments)
- Combine multiple CSS files where possible
- Critical CSS inline in <head> for above-fold content
- Defer non-critical CSS
- Remove unused CSS rules
- Use CSS sprites for small images/icons
JavaScript Optimization:
- Minify JavaScript
- Defer non-critical JS
- Use async loading where appropriate
- Combine scripts to reduce HTTP requests
- Remove unused code
- Consider code splitting for large scripts
Database Query Optimization:
- Use select_related() for foreign key queries
- Use prefetch_related() for reverse foreign key and M2M
- Add database indexes on frequently queried fields
- Cache expensive queries
- Limit query result sets (pagination)
- Avoid N+1 query problems
Caching Strategy:
Template Fragment Caching:
{% load cache %}
{% cache 300 statistics %}
    <div class="statistics">
        <!-- Expensive statistics calculations -->
    </div>
{% endcache %}

View Caching:
from django.views.decorators.cache import cache_page
@cache_page(60 * 5)  # Cache for 5 minutes
def home_view(request):
    ...

Database Query Caching:
from django.core.cache import cache
def get_total_donations():
    total = cache.get('total_donations')
    if total is None:
        total = Donations.objects.filter(
            payment_status='completed'
        ).aggregate(Sum('amount'))['amount__sum']
        cache.set('total_donations', total, 60 * 5)
    return total
Static File Caching:
- Set far-future expiry headers (1 year)
- Version static files (append hash to filename)
- Use Django's ManifestStaticFilesStorage
- Enable GZIP compression on server
- Use CDN for static assets (if budget allows)
Server-Side Optimization:
- Enable GZIP compression in .htaccess:
<IfModule mod_deflate.c>
  AddOutputFilterByType DEFLATE text/html text/css text/javascript
</IfModule>

- Enable browser caching:
<IfModule mod_expires.c>
  ExpiresActive On
  ExpiresByType image/webp "access plus 1 year"
  ExpiresByType text/css "access plus 1 year"
  ExpiresByType text/javascript "access plus 1 year"
</IfModule>

- Enable Keep-Alive for persistent connections
9.2 Monitoring and Testing
Performance Testing Tools:
- Google PageSpeed Insights: Target 90+ score
- GTmetrix: Monitor load time and recommendations
- WebPageTest: Detailed waterfall analysis
- Chrome DevTools Lighthouse: Audit performance
Key Metrics to Monitor:
- Time to First Byte (TTFB): <200ms
- First Contentful Paint (FCP): <1.8s
- Largest Contentful Paint (LCP): <2.5s
- Time to Interactive (TTI): <3.8s
- Total Blocking Time (TBT): <200ms
- Cumulative Layout Shift (CLS): <0.1
Continuous Monitoring:
- Set up Google Analytics with page load time tracking
- Monitor server resources (CPU, RAM, disk usage)
- Track database query performance
- Set up alerts for downtime or slow response times

10. Admin Panel Customization
10.1 Django Admin Configuration
Custom Admin Interface:
File: main_app/admin.py

from django.contrib import admin
from .models import *

# Custom admin site header
admin.site.site_header = "Shree Brijwasi Jatav Samaj Sewa Samiti Admin"
admin.site.site_title = "NGO Admin Portal"
admin.site.index_title = "Welcome to NGO Administration"

# Donations Admin
@admin.register(Donations)
class DonationsAdmin(admin.ModelAdmin):
    list_display = ['transaction_reference', 'donor_name', 'amount', 
                    'payment_status', 'payment_app', 'created_at']
    list_filter = ['payment_status', 'payment_app', 'created_at']
    search_fields = ['donor_name', 'donor_email', 'transaction_reference']
    readonly_fields = ['transaction_reference', 'created_at']
    
    actions = ['mark_as_completed', 'export_to_csv']
    
    def mark_as_completed(self, request, queryset):
        # Custom action to mark multiple donations as completed
        # Send receipt emails
        for donation in queryset:
            donation.mark_completed()
            donation.send_receipt_email()
        self.message_user(request, f"{queryset.count()} donations marked as completed")
    
    def export_to_csv(self, request, queryset):
        # Export selected donations to CSV
        import csv
        from django.http import HttpResponse
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="donations.csv"'
        writer = csv.writer(response)
        writer.writerow(['Reference', 'Donor', 'Email', 'Amount', 'Status', 'Date'])
        for donation in queryset:
            writer.writerow([
                donation.transaction_reference,
                donation.donor_name,
                donation.donor_email,
                donation.amount,
                donation.payment_status,
                donation.created_at
            ])
        return response

# Volunteers Admin
@admin.register(Volunteers)
class VolunteersAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'phone', 'status', 
                    'preferred_area', 'registration_date']
    list_filter = ['status', 'preferred_area', 'availability']
    search_fields = ['name', 'email', 'phone', 'skills']
    readonly_fields = ['registration_date']
    
    actions = ['approve_volunteers', 'send_welcome_email']
    
    def approve_volunteers(self, request, queryset):
        for volunteer in queryset:
            volunteer.approve()
        self.message_user(request, f"{queryset.count()} volunteers approved")

# Contact Submissions Admin
@admin.register(ContactSubmissions)
class ContactSubmissionsAdmin(admin.ModelAdmin):
    list_display = ['subject', 'name', 'email', 'submitted_at', 
                    'is_read', 'is_replied']
    list_filter = ['is_read', 'is_replied', 'submitted_at']
    search_fields = ['name', 'email', 'subject', 'message']
    readonly_fields = ['submitted_at', 'ip_address']
    
    actions = ['mark_as_read', 'mark_as_replied']

# Team Members Admin
@admin.register(TeamMembers)
class TeamMembersAdmin(admin.ModelAdmin):
    list_display = ['name', 'position', 'display_order', 'is_active']
    list_editable = ['display_order', 'is_active']
    search_fields = ['name', 'position']
    list_filter = ['is_active', 'position']

# Work Projects Admin
@admin.register(WorkProjects)
class WorkProjectsAdmin(admin.ModelAdmin):
    list_display = ['title', 'category', 'project_status', 
                    'start_date', 'is_featured', 'is_published']
    list_filter = ['category', 'project_status', 'is_featured', 'is_published']
    search_fields = ['title', 'description']
    prepopulated_fields = {'slug': ('title',)}
    list_editable = ['is_featured', 'is_published']
    
    fieldsets = [
        ('Basic Information', {
            'fields': ['title', 'slug', 'category', 'project_status']
        }),
        ('Description', {
            'fields': ['short_description', 'description']
        }),
        ('Media', {
            'fields': ['featured_image']
        }),
        ('Details', {
            'fields': ['start_date', 'end_date', 'location', 
                      'beneficiaries_count', 'budget', 'partners']
        }),
        ('Publishing', {
            'fields': ['is_featured', 'is_published']
        }),
    ]

# Project Gallery Inline Admin
class ProjectGalleryInline(admin.TabularInline):
    model = ProjectGallery
    extra = 3
    fields = ['image', 'caption', 'display_order']

# Update WorkProjects admin to include gallery inline
WorkProjectsAdmin.inlines = [ProjectGalleryInline]

# Media Gallery Admin
@admin.register(MediaGallery)
class MediaGalleryAdmin(admin.ModelAdmin):
    list_display = ['title', 'media_type', 'category', 'event_date', 
                    'is_featured', 'uploaded_at']
    list_filter = ['media_type', 'category', 'is_featured']
    search_fields = ['title', 'caption']
    list_editable = ['is_featured']

# Site Settings Admin
@admin.register(SiteSettings)
class SiteSettingsAdmin(admin.ModelAdmin):
    fieldsets = [
        ('About Section', {
            'fields': ['about_overview', 'mission_statement', 
                  'vision_statement', 'footer_about_text']
    }),
    ('Statistics', {
        'fields': ['total_beneficiaries', 'total_projects', 
                  'established_year']
    }),
    ('Homepage Content', {
        'fields': ['homepage_hero_title', 'homepage_hero_subtitle',
                  'donation_appeal_text', 'volunteer_appeal_text']
    }),
    ('SEO', {
        'fields': ['meta_description', 'meta_keywords']
    }),
    ('Organization Details', {
        'fields': ['achievements_summary', 'registration_number']
    }),
]

def has_add_permission(self, request):
    # Only allow one SiteSettings instance
    return not SiteSettings.objects.exists()

def has_delete_permission(self, request, obj=None):
    # Prevent deletion of SiteSettings
    return False

### 10.2 Admin Dashboard Enhancements

**Custom Dashboard Widgets:**
Create custom admin views for:

Total donations this month (chart)
Pending volunteer applications count
Unread contact submissions count
Recent activity feed
Quick stats overview

Add to admin index template override

**Admin Shortcuts:**
Quick action buttons:

"Add New Project"
"Review Pending Volunteers"
"Verify Donations"
"Upload Media"


---

## 11. Email System Configuration

### 11.1 Email Templates

**HTML Email Template Structure:**
Base Email Template (templates/emails/base_email.html):

NGO logo header
Main content area (block content)
Footer with contact info and social links
Unsubscribe link (for newsletters)
Responsive design for mobile

Child templates extend base and fill content block

**Email Types:**

**1. Donation Confirmation (Pending):**
Subject: Thank you for your donation - Pending Verification
Content:

Personalized greeting
Transaction reference number
Amount donated
Pending status explanation
Estimated verification time
Contact for queries


**2. Donation Receipt (Completed):**
Subject: Donation Receipt - [Transaction Reference]
Content:

Official receipt format
NGO registration details
Donor details
Amount and date
Transaction ID
Tax benefit information
Thank you message
PDF attachment option


**3. Volunteer Welcome:**
Subject: Thank you for registering - Application Received
Content:

Welcome message
Application received confirmation
Review timeline
What to expect next
Resources for volunteers


**4. Volunteer Approval:**
Subject: Volunteer Application Approved!
Content:

Congratulations
Onboarding information
Next steps
Coordinator contact
Orientation details


**5. Contact Auto-Reply:**
Subject: We received your message
Content:

Acknowledgment
Expected response time
Alternative contact methods
Copy of their message


**6. Admin Notifications:**
New Donation: Alert with details and verification link
New Volunteer: Alert with details and approval link
New Contact: Alert with message details

### 11.2 Email Sending Configuration

**Django Email Settings:**
In config.py:
EMAIL_CONFIG = {
'EMAIL_BACKEND': 'django.core.mail.backends.smtp.EmailBackend',
'EMAIL_HOST': 'smtp.gmail.com',  # or other SMTP server
'EMAIL_PORT': 587,
'EMAIL_USE_TLS': True,
'EMAIL_HOST_USER': 'ngo@yourdomain.com',
'EMAIL_HOST_PASSWORD': 'your_email_password',
'DEFAULT_FROM_EMAIL': 'Shree Brijwasi Jatav Samaj Sewa Samiti ngo@yourdomain.com',
}
For development:
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
(Prints emails to console instead of sending)

**Email Utility Functions:**
File: main_app/utils.py
from django.core.mail import send_mail, EmailMultiAlternatives
from django.template.loader import render_to_string
from django.conf import settings
def send_templated_email(subject, template_name, context, recipient_list):
"""
Send HTML email using template
"""
html_content = render_to_string(f'emails/{template_name}', context)
email = EmailMultiAlternatives(
    subject=subject,
    body=html_content,  # Fallback plain text
    from_email=settings.DEFAULT_FROM_EMAIL,
    to=recipient_list
)
email.attach_alternative(html_content, "text/html")
email.send()
def send_donation_confirmation(donation):
"""
Send confirmation email for pending donation
"""
context = {
'donor_name': donation.donor_name,
'amount': donation.amount,
'transaction_reference': donation.transaction_reference,
}
send_templated_email(
subject='Thank you for your donation - Pending Verification',
template_name='donation_confirmation.html',
context=context,
recipient_list=[donation.donor_email]
)
def send_donation_receipt(donation):
"""
Send receipt email for completed donation
"""
context = {
'donation': donation,
'ngo_name': settings.SITE_CONFIG['SITE_NAME'],
'registration_number': SiteSettings.get_settings().registration_number,
}
send_templated_email(
subject=f'Donation Receipt - {donation.transaction_reference}',
template_name='donation_receipt.html',
context=context,
recipient_list=[donation.donor_email]
)
# Optionally attach PDF receipt
def send_volunteer_welcome(volunteer):
"""
Send welcome email to new volunteer applicant
"""
context = {
'volunteer': volunteer,
}
send_templated_email(
subject='Thank you for volunteering - Application Received',
template_name='volunteer_welcome.html',
context=context,
recipient_list=[volunteer.email]
)
def send_volunteer_approval(volunteer):
"""
Send approval email to volunteer
"""
context = {
'volunteer': volunteer,
}
send_templated_email(
subject='Volunteer Application Approved!',
template_name='volunteer_approved.html',
context=context,
recipient_list=[volunteer.email]
)
def send_contact_auto_reply(submission):
"""
Send auto-reply to contact form submission
"""
context = {
'submission': submission,
}
send_templated_email(
subject='We received your message',
template_name='contact_auto_reply.html',
context=context,
recipient_list=[submission.email]
)
def send_admin_notification(subject, message, context=None):
"""
Send notification to admin
"""
admin_emails = ['admin@ngo.com']  # From config
send_templated_email(
subject=subject,
template_name='admin_notification.html',
context=context or {'message': message},
recipient_list=admin_emails
)

---

## 12. Testing and Quality Assurance

### 12.1 Testing Checklist

**Functional Testing:**
Home Page:
☐ Slider rotates images automatically
☐ Statistics display correctly
☐ Featured projects load
☐ CTA buttons link correctly
☐ Page loads in <3 seconds
About Pages:
☐ Overview displays mission/vision
☐ Team members display with photos
☐ Team member order follows display_order
☐ Modal opens with full bio
Our Work:
☐ Projects filter by category
☐ Projects filter by status
☐ Pagination works correctly
☐ Project detail page displays all info
☐ Gallery lightbox functions
☐ Related projects appear
Donation:
☐ Amount validation works
☐ Pre-defined amounts populate field
☐ Custom amount can be entered
☐ UPI app selection required
☐ Form validation prevents empty fields
☐ Deep link generated correctly
☐ Transaction reference created
☐ Confirmation email sent
☐ Admin notification sent
☐ Receipt sent on completion
Volunteer:
☐ All fields validate correctly
☐ Email uniqueness checked
☐ Form submits successfully
☐ Volunteer record created
☐ Welcome email sent
☐ Admin notification sent
☐ Approval email sent when approved
Media:
☐ Gallery displays all media
☐ Filter by category works
☐ Filter by media type works
☐ Lightbox opens images
☐ Videos play in modal
☐ Lazy loading works
Contact:
☐ Form validates fields
☐ reCAPTCHA validates
☐ Submission saved to database
☐ Auto-reply sent
☐ Admin notification sent
☐ Map displays correctly

**Cross-Browser Testing:**
Test on:
☐ Chrome (latest)
☐ Firefox (latest)
☐ Safari (latest)
☐ Edge (latest)
☐ Mobile Safari (iOS)
☐ Chrome Mobile (Android)

**Responsive Design Testing:**
Test on:
☐ Desktop (1920x1080)
☐ Laptop (1366x768)
☐ Tablet (768x1024)
☐ Mobile (375x667)
☐ Large Mobile (414x896)

**Performance Testing:**
☐ Homepage loads in <3 seconds
☐ Images optimized and compressed
☐ CSS and JS minified
☐ Lazy loading implemented
☐ Caching configured correctly
☐ Google PageSpeed score >90

**Security Testing:**
☐ SQL injection prevention verified
☐ XSS prevention verified
☐ CSRF tokens on all forms
☐ File upload validation working
☐ Admin requires strong password
☐ HTTPS enforced
☐ Sensitive data encrypted

### 12.2 User Acceptance Testing (UAT)

**UAT Scenarios:**

New visitor arrives at homepage

Can they understand NGO mission?
Is navigation intuitive?
Do CTAs motivate action?


Donor wants to contribute

Can they easily find donation page?
Is donation process clear?
Do they receive confirmation?


Volunteer wants to register

Is form easy to complete?
Are requirements clear?
Do they know next steps?


Person has a question

Can they find contact info easily?
Is contact form simple?
Do they get acknowledgment?


Admin needs to manage content

Can they log in easily?
Is admin interface intuitive?
Can they update content without errors?




---

## 13. Documentation and Handover

### 13.1 User Documentation

**Admin User Guide:**
Topics to cover:

Logging into admin panel
Managing donations (verifying, marking complete)
Reviewing and approving volunteers
Adding/editing team members
Creating and publishing work projects
Uploading media to gallery
Updating site settings
Responding to contact submissions
Exporting data to CSV
Backup and security best practices


**Content Update Guide:**
Step-by-step instructions for:

Adding a new team member with photo
Publishing a new work project
Adding gallery images to a project
Uploading media items
Editing homepage content
Updating mission/vision statements
Changing contact information


### 13.2 Technical Documentation

**Developer Handover Document:**

Project structure overview
Technology stack details
Configuration file locations
Database schema with ERD
View function descriptions
Template hierarchy
Static file organization
Email system workflow
Payment flow diagram
Deployment procedures
Troubleshooting guide
Future enhancement suggestions


**README.md File:**
Shree Brijwasi Jatav Samaj Sewa Samiti Website
Overview
Brief description of the project
Technology Stack

Django 4.2+
MySQL 8.0+
HTML5, CSS3, JavaScript
Bootstrap 5

Local Development Setup

Clone repository
Create virtual environment
Install dependencies
Configure database
Run migrations
Create superuser
Run development server

Deployment to cPanel
Step-by-step deployment instructions
Configuration
Explanation of config files
Features
List of main features
Admin Access
URL, default credentials (change immediately)
Contact
Developer contact information

---

## 14. Future Enhancements (Optional)

**Phase 2 Features (Post-Launch):**

Newsletter system for subscribers
Event management and registration
Impact stories blog section
Beneficiary testimonials
Annual report generation
Advanced donation tracking and reporting
Volunteer portal with dashboard
Online community forum
Integration with social media for auto-posting
Multi-language support (Hindi, English)
Mobile app for donors and volunteers
Recurring donation subscriptions
Crowdfunding for specific projects
Integration with third-party payment gateways (Razorpay, Paytm)
Advanced analytics and impact metrics dashboard


---

## 15. Conclusion

This Product Requirements Document provides a comprehensive blueprint for developing the Shree Brijwasi Jatav Samaj Sewa Samiti NGO website. The architecture emphasizes simplicity through single-file-per-page views, centralized configuration for easy deployment, and reusable components to minimize code duplication.

**Key Success Factors:**
1. **Simplicity**: Easy to develop, maintain, and deploy
2. **Portability**: Works on localhost (XAMPP) and cPanel without code changes
3. **Security**: Django best practices, CSRF protection, input validation
4. **Performance**: Homepage loads in ≤3 seconds
5. **Functionality**: Complete donation, volunteer, and content management systems
6. **Scalability**: Database schema and code structure support future growth

**Deployment Readiness:**
The single configuration file approach ensures that moving from development to production requires only updating database credentials and domain settings in `config_production.py`. All business logic, templates, and static files remain unchanged.

**Success Metrics:**
- Homepage load time ≤3 seconds
- 100% form submission success rate
- Zero security vulnerabilities
- Admin can manage all content without developer assistance
- Mobile responsive on all devices
- 90+ Google PageSpeed score

This PRD serves as the definitive guide for developers, admins, and stakeholders throughout the development lifecycle and beyond.