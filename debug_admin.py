import os
import django
import sys

# Add current directory to path
sys.path.append(os.getcwd())

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ngo_website.settings')
django.setup()

from django.contrib import admin
from django import forms

def check_admin_class(model, admin_class):
    print(f"Checking {model.__name__} Admin...")
    ma = admin_class(model, admin.site)
    
    # Check list_display
    ld = ma.get_list_display(None)
    for field_name in ld:
        if field_name == '__str__': continue
        if hasattr(ma, field_name): continue
        if hasattr(model, field_name): continue
        # Check if it's a method on the model
        if hasattr(model, f"get_{field_name}_display"): continue
        print(f"  [ERROR] list_display: '{field_name}' not found on model or admin.")

    # Check list_filter
    lf = ma.get_list_filter(None)
    for field_name in lf:
        if isinstance(field_name, (list, tuple)):
            field_name = field_name[0]
        if not hasattr(model, field_name):
             print(f"  [ERROR] list_filter: '{field_name}' not found on model.")

    # Check fieldsets
    fs = ma.get_fieldsets(None)
    for label, info in fs:
        fields = info.get('fields', [])
        for field in fields:
            if isinstance(field, (list, tuple)):
                items = field
            else:
                items = [field]
            for item in items:
                if hasattr(ma, item): continue
                if hasattr(model, item): continue
                print(f"  [ERROR] fieldsets: '{item}' not found on model or admin.")

    # Check readonly_fields
    rf = ma.get_readonly_fields(None)
    for field in rf:
        if hasattr(ma, field): continue
        if hasattr(model, field): continue
        print(f"  [ERROR] readonly_fields: '{field}' not found on model or admin.")

# Get all registered models
for model, ma in admin.site._registry.items():
    check_admin_class(model, type(ma))
