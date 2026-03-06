# NGO Website Deployment Guide

## 🚀 Your Website is Ready for Global Hosting!

This guide will help you deploy your Django NGO website to production. Choose the hosting platform that best fits your needs.

---

## 📋 **Pre-Deployment Checklist**

### ✅ **Required Information**
- [ ] **Domain Name** (e.g., yourngo.org)
- [ ] **UPI ID** for donations (e.g., yourngo@okaxis)
- [ ] **Email Account** for sending receipts
- [ ] **Contact Details** (phone, address)
- [ ] **Social Media Links** (optional)

### ✅ **Update Admin Settings**
1. Go to `http://127.0.0.1:8000/admin/`
2. Click **"Site Settings"**
3. Fill in:
   - Contact Email, Phone, Address
   - Social Media Links (JSON format)
   - UPI ID for donations
4. Save changes

---

## 🔧 **Settings Configuration**

Your project includes **3 settings files**:

### **1. `settings.py`** - Development (current)
- For local development
- Uses config/config.py

### **2. `settings_production.py`** - Advanced Production
- Requires: `python-decouple`, `dj-database-url`
- Supports: Heroku, advanced platforms
- Auto-detects DATABASE_URL

### **3. `settings_simple.py`** - Basic Production
- No extra dependencies required
- Uses: SQLite + environment variables
- Perfect for: cPanel, basic hosting

---

## 🌐 **Deployment Options**

### **Option 1: Heroku (Easiest - Free Tier Available)**

#### **Step 1: Install Heroku CLI**
```bash
# Download from: https://devcenter.heroku.com/articles/heroku-cli
# Or using npm: npm install -g heroku
```

#### **Step 2: Prepare for Heroku**
```bash
# Login to Heroku
heroku login

# Create Heroku app
heroku create your-ngo-website-name

# Set environment variables
heroku config:set DJANGO_SETTINGS_MODULE=ngo_website.settings_production
heroku config:set SECRET_KEY=your-random-secret-key-here
heroku config:set DEBUG=False
heroku config:set ALLOWED_HOSTS=your-ngo-website-name.herokuapp.com
heroku config:set EMAIL_HOST=your-email-host
heroku config:set EMAIL_HOST_USER=your-email@domain.com
heroku config:set EMAIL_HOST_PASSWORD=your-email-password
heroku config:set UPI_VPA=your-upi-id@okaxis
```

#### **Step 3: Deploy**
```bash
# Add files to git (if not already)
git init
git add .
git commit -m "Initial commit"

# Deploy to Heroku
git push heroku main

# Create database tables
heroku run python manage.py migrate

# Create admin user
heroku run python manage.py createsuperuser

# Collect static files
heroku run python manage.py collectstatic --noinput
```

#### **Step 4: Access Your Site**
- **Website**: `https://your-ngo-website-name.herokuapp.com/`
- **Admin**: `https://your-ngo-website-name.herokuapp.com/admin/`

---

### **Option 2: DigitalOcean App Platform (User-Friendly)**

1. **Sign up** at [DigitalOcean](https://digitalocean.com)
2. **Create App** → Choose "Django"
3. **Connect Repository** → Upload your code
4. **Configure Environment Variables** (same as Heroku)
5. **Deploy**

---

### **Option 3: cPanel/Shared Hosting (Traditional)**

#### **Step 1: Get Hosting**
- Bluehost, HostGator, or any cPanel hosting
- Ensure Python support (Python 3.11+)

#### **Step 2: Upload Files**
```bash
# Use FTP or cPanel File Manager
# Upload all files to public_html/ or subdomain folder
```

#### **Step 3: Configure Database**
1. Create MySQL database in cPanel
2. Update `.env` file with database credentials

#### **Step 4: Install Dependencies**
```bash
# Via SSH or cPanel Terminal
pip install -r requirements.txt
```

#### **Step 3: Configure Passenger WSGI**
Create `passenger_wsgi.py` in your project root:
```python
import os
import sys

# Add project directory to path
sys.path.insert(0, os.path.dirname(__file__))

# Set environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ngo_website.settings_simple')

# Import Django
import django
django.setup()

# Import WSGI application
from ngo_website.wsgi import application
```

**Note:** For cPanel, use `settings_simple.py` instead of `settings_production.py` since it doesn't require additional packages.

#### **Step 6: Set Up Domain**
- Point domain to hosting
- Configure SSL certificate

---

### **Option 4: VPS (Linode/AWS/DigitalOcean Droplet) - Advanced**

#### **Step 1: Server Setup**
```bash
# Update system
sudo apt update && sudo apt upgrade

# Install Python and pip
sudo apt install python3 python3-pip python3-venv

# Install Nginx
sudo apt install nginx

# Install PostgreSQL (recommended for production)
sudo apt install postgresql postgresql-contrib
```

#### **Step 2: Application Setup**
```bash
# Clone your repository
git clone https://github.com/yourusername/ngo-website.git
cd ngo-website

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
pip install gunicorn psycopg2-binary

# Environment variables
cp .env.example .env
nano .env  # Edit with your values
```

#### **Step 3: Database Setup**
```bash
# Create PostgreSQL database
sudo -u postgres psql
CREATE DATABASE ngo_db;
CREATE USER ngo_user WITH PASSWORD 'your_password';
GRANT ALL PRIVILEGES ON DATABASE ngo_db TO ngo_user;
\q

# Run migrations
python manage.py migrate
```

#### **Step 4: Gunicorn Setup**
Create `/etc/systemd/system/gunicorn.service`:
```ini
[Unit]
Description=gunicorn daemon
After=network.target

[Service]
User=ubuntu
Group=www-data
WorkingDirectory=/home/ubuntu/ngo-website
ExecStart=/home/ubuntu/ngo-website/venv/bin/gunicorn --access-logfile - --workers 3 --bind unix:/home/ubuntu/ngo-website/app.sock ngo_website.wsgi:application

[Install]
WantedBy=multi-user.target
```

#### **Step 5: Nginx Configuration**
Create `/etc/nginx/sites-available/ngo_website`:
```nginx
server {
    listen 80;
    server_name yourdomain.com www.yourdomain.com;

    location = /favicon.ico { access_log off; log_not_found off; }

    location /static/ {
        alias /home/ubuntu/ngo-website/staticfiles/;
    }

    location /media/ {
        alias /home/ubuntu/ngo-website/media/;
    }

    location / {
        include proxy_params;
        proxy_pass http://unix:/home/ubuntu/ngo-website/app.sock;
    }
}
```

#### **Step 6: SSL with Certbot**
```bash
# Install Certbot
sudo apt install certbot python3-certbot-nginx

# Get SSL certificate
sudo certbot --nginx -d yourdomain.com -d www.yourdomain.com
```

---

## 🔧 **Post-Deployment Tasks**

### **1. Update Site Settings**
- Go to `https://yourdomain.com/admin/`
- Update contact information, UPI ID, etc.

### **2. Test Everything**
- [ ] Homepage loads
- [ ] Contact form works
- [ ] Donation form works
- [ ] Admin panel accessible
- [ ] SSL certificate active
- [ ] Email sending works

### **3. SEO & Analytics**
- Add Google Analytics
- Submit sitemap to Google Search Console
- Set up Google My Business

---

## 🆘 **Troubleshooting**

### **Common Issues:**

**"Application Error" on Heroku:**
```bash
heroku logs --tail
# Check for missing environment variables or build errors
```

**Static files not loading:**
```bash
python manage.py collectstatic --noinput
```

**Database connection issues:**
- Check DATABASE_URL format
- Ensure database credentials are correct

**Email not sending:**
- Verify EMAIL_HOST settings
- Check spam folder

---

## 💰 **Cost Comparison**

| Platform | Free Tier | Paid Plans | Best For |
|----------|-----------|------------|----------|
| Heroku | 550-1000 hours/month | $7+/month | Quick deployment |
| DigitalOcean App | No free | $12+/month | Simple hosting |
| cPanel Hosting | No free | $3-10/month | Traditional hosting |
| VPS | No free | $5+/month | Full control |

---

## 🎯 **Recommended: Start with Heroku**

For your NGO website, I recommend **Heroku** because:
- ✅ Free tier available
- ✅ Easy deployment
- ✅ Automatic SSL
- ✅ Good performance for small-medium sites
- ✅ Simple scaling when needed

**Ready to deploy?** Let me know which option you prefer, and I can help you with the specific steps!

---

## 📞 **Need Help?**

If you run into any issues during deployment:
1. Check the error logs
2. Verify environment variables
3. Ensure all requirements are installed
4. Test locally first with production settings

Your website will be live globally once deployed! 🌍