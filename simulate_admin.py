import os
import django
import sys
from django.conf import settings
from django.contrib.admin.sites import AdminSite
from django.test import RequestFactory

# Set up Django environment
sys.path.append(os.getcwd())
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ngo_website.settings')
django.setup()

from main.models import WorkProject, SiteSettings
from main.admin import WorkProjectAdmin, SiteSettingsAdmin

def debug_admin_rendering(model, admin_class, url):
    print(f"\n--- Debugging {model.__name__} Admin Rendering ---")
    site = AdminSite()
    ma = admin_class(model, site)
    rf = RequestFactory()
    request = rf.get(url)
    
    # Simulate a superuser request
    from django.contrib.auth.models import User
    admin_user = User.objects.filter(is_superuser=True).first()
    if not admin_user:
        # Create a temp superuser if none exists
        admin_user = User.objects.create_superuser('temp_admin', 'admin@example.com', 'pass')
    
    request.user = admin_user
    
    try:
        # Check changelist rendering
        print("Checking ChangeList...")
        cl = ma.get_changelist_instance(request)
        print("Successfully got ChangeList instance.")
        
        # Check individual object change form
        obj = model.objects.first()
        if obj:
            print(f"Checking Change Form for object ID: {obj.id}...")
            ma.get_form(request, obj)
            print("Successfully got Change Form.")
        else:
            print("No objects found to test Change Form.")
            
    except Exception as e:
        import traceback
        print(f"ERROR: Caught exception during {model.__name__} rendering:")
        print(traceback.format_exc())

# Test WorkProject
debug_admin_rendering(WorkProject, WorkProjectAdmin, '/admin/main/workproject/')

# Test SiteSettings
debug_admin_rendering(SiteSettings, SiteSettingsAdmin, '/admin/main/sitesettings/')
