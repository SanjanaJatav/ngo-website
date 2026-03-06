# NGO Website - Full Stack Django Application

## Project Overview
This is a complete full-stack website for **Shree Brijwasi Jatav Samaj Sewa Samiti**, an NGO dedicated to social empowerment and community service. The website includes donation management, volunteer registration, project showcase, media gallery, and more.

## Features
- ✅ **Responsive Design** - Works perfectly on desktop, tablet, and mobile
- ✅ **UPI Payment Integration** - Accept donations via Google Pay, PhonePe, Paytm, BHIM
- ✅ **Volunteer Management** - Registration and approval system
- ✅ **Project Showcase** - Display ongoing and completed work
- ✅ **Media Gallery** - Photos and videos from events
- ✅ **Contact Forms** - Easy communication with the organization
- ✅ **Admin Panel** - Full Django admin for content management
- ✅ **Email Notifications** - Automatic emails for donations, volunteers, and contacts
- ✅ **Dynamic Configuration** - Single file deployment from localhost to cPanel

## Technology Stack
- **Backend**: Django 4.2+
- **Frontend**: HTML5, CSS3, JavaScript (ES6+)
- **Database**: MySQL 8.0+
- **Styling**: Bootstrap 5 + Custom CSS
- **Icons**: Font Awesome 6
- **Fonts**: Google Fonts (Inter, Poppins)

## Installation & Setup

### Prerequisites
- Python 3.9+
- MySQL 8.0+
- Git (optional)

### Step 1: Clone or Download
```bash
# If using git
git clone <repository-url>
cd "ngo website"

# Or extract the ZIP file to your desired location
```

### Step 2: Create Virtual Environment (Recommended)
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Linux/Mac
python3 -m venv venv
source venv/bin/activate
```

### Step 3: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 4: Configure Database
1. Start XAMPP and ensure MySQL is running
2. Create a database:
```sql
CREATE DATABASE ngo_website_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
```

3. Update `config/config.py` if needed (default settings should work with XAMPP)

### Step 5: Run Migrations
```bash
python manage.py makemigrations
python manage.py migrate
```

### Step 6: Create Superuser (Admin Account)
```bash
python manage.py createsuperuser
```
Follow the prompts to create your admin account.

### Step 7: Collect Static Files (Optional for development)
```bash
python manage.py collectstatic
```

### Step 8: Run Development Server
```bash
python manage.py runserver
```

Visit: http://127.0.0.1:8000/

Admin Panel: http://127.0.0.1:8000/admin/

## Configuration

### Central Configuration File
All environment-specific settings are in `config/config.py`:

- **Database Settings**: MySQL connection details
- **Email Settings**: SMTP configuration
- **Payment Settings**: UPI details for donations
- **Site Information**: NGO name, contact details, social media links
- **Media Settings**: Upload paths and file restrictions

### Deployment to cPanel

1. Update `config/config.py` with production database credentials
2. Update production email settings
3. Update UPI payment details with actual NGO UPI ID
4. Upload all files to cPanel
5. Run migrations on production: `python manage.py migrate`
6. Create superuser on production
7. Configure static files path in cPanel

The system automatically detects whether it's running on localhost or production and uses appropriate settings!

## Adding Content

### Via Django Admin
1. Login to admin panel: `/admin/`
2. **Site Settings**: Update mission, vision, about text
3. **Team Members**: Add leadership and team profiles
4. **Work Projects**: Add your organization's projects
5. **Media Gallery**: Upload photos and videos
6. **Donations**: View and verify payments
7. **Volunteers**: Review and approve applications

### Adding Images
Place images in the following directories:
- `static/images/` - General website images
- `static/images/slider/` - Hero slider backgrounds (slide1.jpg, slide2.jpg, slide3.jpg)
- `media/team_photos/` - Team member photos (uploaded via admin)
- `media/work_projects/` - Project featured images (uploaded via admin)

## File Structure
```
ngo website/
├── config/
│   ├── __init__.py
│   └── config.py              # Central configuration
├── main/
│   ├── migrations/
│   ├── __init__.py
│   ├── admin.py              # Admin configuration
│   ├── apps.py
│   ├── context_processors.py # Template context
│   ├── models.py             # Database models
│   ├── urls.py               # URL patterns
│   └── views.py              # View functions
├── ngo_website/
│   ├── __init__.py
│   ├── asgi.py
│   ├── settings.py           # Django settings
│   ├── urls.py               # Main URL config
│   └── wsgi.py
├── static/
│   ├── css/
│   │   └── styles.css        # Custom styles
│   ├── js/
│   │   └── main.js           # JavaScript
│   └── images/               # Static images
├── templates/
│   ├── base.html             # Base template
│   ├── home.html             # Homepage
│   ├── about_overview.html
│   ├── team.html
│   ├── our_work.html
│   ├── project_detail.html
│   ├── donate.html
│   ├── donation_thank_you.html
│   ├── volunteer.html
│   ├── volunteer_thank_you.html
│   ├── contact.html
│   └── media.html
├── media/                    # User uploads (created automatically)
├── manage.py
├── requirements.txt
└── README.md
```

## UPI Payment Setup

### Configure Your UPI Details
Edit `config/config.py`:

```python
PAYMENT_CONFIG = {
    'UPI_VPA': 'your-ngo@okaxis',  # Replace with your UPI ID
    'UPI_PAYEE_NAME': 'Your NGO Name',
    'SUPPORTED_UPI_APPS': ['googlepay', 'phonepe', 'paytm', 'bhim', 'other'],
    'MINIMUM_DONATION': 100,
   'CURRENCY': 'INR',
    'TRANSACTION_PREFIX': 'SBJS',  # Change to your prefix
}
```

### How Payment Works
1. User selects amount and enters details
2. System generates unique transaction reference
3. Creates UPI deep link with amount and reference
4. User completes payment in their UPI app
5. Admin verifies payment manually in admin panel
6. System sends receipt email to donor

## Email Configuration

### For Development (Console Backend)
Emails print to console - already configured in `config.py`

### For Production (SMTP)
Update in `config/config.py`:

```python
EMAIL_CONFIG = {
    'EMAIL_BACKEND': 'django.core.mail.backends.smtp.EmailBackend',
    'EMAIL_HOST': 'mail.yourdomain.com',
    'EMAIL_PORT': 587,
    'EMAIL_USE_TLS': True,
    'EMAIL_HOST_USER': 'noreply@yourdomain.com',
    'EMAIL_HOST_PASSWORD': 'your-password',
    'DEFAULT_FROM_EMAIL': 'NGO Name <noreply@yourdomain.com>',
}
```

## Customization

### Colors and Branding
Edit `config/config.py`:

```python
SITE_CONFIG = {
    'LOGO_PRIMARY_COLOR': '#2563eb',    # Your brand color
    'LOGO_SECONDARY_COLOR': '#7c3aed',  # Accent color
    # ... other settings
}
```

### Adding New Pages
1. Create view function in `main/views.py`
2. Add URL pattern in `main/urls.py`
3. Create template in `templates/`
4. Add navigation link in `templates/base.html`

## Security Notes

### Before Going Live
1. Change `SECRET_KEY` in `ngo_website/settings.py`
2. Set `DEBUG = False` in production
3. Update `ALLOWED_HOSTS` with your domain
4. Enable HTTPS/SSL
5. Update payment details with real UPI ID
6. Configure real SMTP email settings
7. Regular database backups

## Troubleshooting

### Database Connection Error
- Ensure MySQL is running in XAMPP
- Verify database name and credentials in `config/config.py`
- Check if database exists: `SHOW DATABASES;`

### Static Files Not Loading
- Run: `python manage.py collectstatic`
- Check `STATIC_URL` and `STATIC_ROOT` in settings

### Images Not Uploading
- Check `MEDIA_ROOT` and `MEDIA_URL` settings
- Ensure `media/` directory has write permissions

### Email Not Sending
- For development, check console output
- For production, verify SMTP credentials
- Check firewall/port 587 accessibility

## Support & Documentation

- Django Documentation: https://docs.djangoproject.com/
- Bootstrap Documentation: https://getbootstrap.com/docs/
- Font Awesome Icons: https://fontawesome.com/icons

## License
This project is created for Shree Brijwasi Jatav Samaj Sewa Samiti.

## Credits
- Design & Development: Professional Full-Stack Implementation
- Framework: Django
- UI Framework: Bootstrap 5
- Icons: Font Awesome 6
- Fonts: Google Fonts (Inter, Poppins)

---

**For questions or support, please contact the development team.**
