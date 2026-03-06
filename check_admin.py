import os
import django
import sys

# Add current directory to path
sys.path.append(os.getcwd())

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ngo_website.settings')
django.setup()

from main.models import WorkProject, SiteSettings
from main.admin import WorkProjectAdmin, SiteSettingsAdmin
from django.contrib.admin.sites import AdminSite

site = AdminSite()

print("--- Checking WorkProject ---")
try:
    wp_admin = WorkProjectAdmin(WorkProject, site)
    for field in wp_admin.get_list_display(None):
        if callable(field): continue
        if not hasattr(WorkProject, field) and not hasattr(wp_admin, field):
            print(f"Error: WorkProject has no attribute '{field}' (list_display)")
    
    for fs in wp_admin.get_fieldsets(None):
        for field in fs[1]['fields']:
            if not hasattr(WorkProject, field):
                print(f"Error: WorkProject has no attribute '{field}' (fieldsets)")
except Exception as e:
    print(f"Exception checking WorkProject: {e}")

print("\n--- Checking SiteSettings ---")
try:
    ss_admin = SiteSettingsAdmin(SiteSettings, site)
    for fs in ss_admin.get_fieldsets(None):
        for field in fs[1]['fields']:
            if not hasattr(SiteSettings, field):
                print(f"Error: SiteSettings has no attribute '{field}' (fieldsets)")
except Exception as e:
    print(f"Exception checking SiteSettings: {e}")
