# Shree Brijwasi Jatav Samaj Sewa Samiti - Full Stack NGO Website

A complete, production-ready Django website for an NGO with donation management, volunteer registration, and content management.

## Quick Start Guide

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Configure Database
Create MySQL database:
```sql
CREATE DATABASE ngo_website_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
```

### 3. Run Migrations
```bash
python manage.py makemigrations
python manage.py migrate
```

### 4. Create Admin User
```bash
python manage.py createsuperuser
```

### 5. Run Server
```bash
python manage.py runserver
```

Visit: **http://127.0.0.1:8000/**

---

## Features Implemented

✅ **Modern Responsive Design** - Beautiful UI with gradients and animations  
✅ **UPI Payment Integration** - Google Pay, PhonePe, Paytm, BHIM  
✅ **Donation Management** - Full tracking and email receipts  
✅ **Volunteer System** - Registration, approval, and notifications  
✅ **Project Showcase** - Filterable project gallery  
✅ **Media Gallery** - Photos and videos with lightbox  
✅ **Contact Forms** - Automated email notifications  
✅ **Admin Panel** - Complete Django admin interface  
✅ **Configuration System** - Single-file deployment setup  

## Project Structure

- **config/** - Central configuration for easy deployment
- **main/** - Main Django app with all business logic
- **templates/** - Beautiful HTML templates
- **static/** - CSS, JavaScript, and images
- **media/** - User-uploaded content

## Next Steps

1. **Add Images**: Place slider images in `static/images/slider/`
2. **Update Config**: Edit `config/config.py` with your UPI ID and contact details
3. **Add Content**: Login to `/admin/` and add team members, projects, etc.
4. **Customize**: Update colors, branding, and content

## Documentation

See the full [README.md](README.md) for detailed documentation.

---

**Built with Django 4.2+ | Bootstrap 5 | Modern JavaScript**
