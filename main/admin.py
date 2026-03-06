"""
Django admin configuration for all models
"""

from django.contrib import admin
from .models import (
    Donation, Volunteer, ContactSubmission, TeamMember,
    WorkProject, ProjectGallery, MediaGallery, SiteSettings,
    SliderImage, SiteStatistics
)


@admin.register(Donation)
class DonationAdmin(admin.ModelAdmin):
    list_display = ['donor_name', 'amount', 'payment_status', 'payment_app', 'created_at', 'receipt_sent']
    list_filter = ['payment_status', 'payment_app', 'is_anonymous', 'receipt_sent']
    search_fields = ['donor_name', 'donor_email', 'transaction_reference', 'upi_transaction_id']
    readonly_fields = ['transaction_reference', 'created_at', 'completed_at']
    fieldsets = (
        ('Donor Information', {
            'fields': ('donor_name', 'donor_email', 'donor_phone', 'is_anonymous')
        }),
        ('Payment Details', {
            'fields': ('amount', 'payment_app', 'payment_status', 'upi_transaction_id', 'transaction_reference')
        }),
        ('Additional Information', {
            'fields': ('donation_purpose', 'receipt_sent', 'notes')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'completed_at')
        }),
    )
    
    actions = ['mark_as_completed']
    
    @admin.action(description="Mark selected donations as completed")
    def mark_as_completed(self, request, queryset):
        for donation in queryset:
            if donation.payment_status == 'pending':
                donation.mark_completed(f"MANUAL_{donation.transaction_reference}")
        self.message_user(request, f"{queryset.count()} donations marked as completed.")


@admin.register(Volunteer)
class VolunteerAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'phone', 'status', 'preferred_area', 'registration_date']
    list_filter = ['status', 'preferred_area', 'availability', 'is_active']
    search_fields = ['name', 'email', 'phone', 'skills']
    readonly_fields = ['registration_date', 'approved_date']
    fieldsets = (
        ('Personal Information', {
            'fields': ('name', 'email', 'phone', 'age', 'address')
        }),
        ('Volunteer Details', {
            'fields': ('skills', 'availability', 'preferred_area', 'experience', 'message')
        }),
        ('Status & Approval', {
            'fields': ('status', 'approved_date', 'approved_by', 'is_active')
        }),
        ('Emergency Contact', {
            'fields': ('emergency_contact_name', 'emergency_contact_phone')
        }),
        ('Communication', {
            'fields': ('newsletter_subscription', 'registration_date')
        }),
    )
    
    actions = ['approve_volunteers']
    
    @admin.action(description="Approve selected volunteers")
    def approve_volunteers(self, request, queryset):
        for volunteer in queryset:
            if volunteer.status == 'pending':
                volunteer.approve(request.user)
        self.message_user(request, f"{queryset.count()} volunteers approved.")


@admin.register(ContactSubmission)
class ContactSubmissionAdmin(admin.ModelAdmin):
    list_display = ['subject', 'name', 'email', 'submitted_at', 'is_read', 'is_replied']
    list_filter = ['is_read', 'is_replied', 'submitted_at']
    search_fields = ['name', 'email', 'subject', 'message']
    readonly_fields = ['submitted_at', 'ip_address']
    fieldsets = (
        ('Contact Information', {
            'fields': ('name', 'email', 'phone', 'ip_address')
        }),
        ('Message', {
            'fields': ('subject', 'message')
        }),
        ('Status', {
            'fields': ('is_read', 'is_replied', 'replied_at', 'admin_notes', 'submitted_at')
        }),
    )
    
    actions = ['mark_as_read']
    
    @admin.action(description="Mark selected as read")
    def mark_as_read(self, request, queryset):
        queryset.update(is_read=True)
        self.message_user(request, f"{queryset.count()} submissions marked as read.")


@admin.register(TeamMember)
class TeamMemberAdmin(admin.ModelAdmin):
    list_display = ['name', 'position', 'display_order', 'is_active', 'joined_date']
    list_filter = ['is_active', 'joined_date']
    search_fields = ['name', 'position', 'bio']
    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'position', 'photo', 'bio')
        }),
        ('Contact Information', {
            'fields': ('email', 'phone', 'social_media_links')
        }),
        ('Settings', {
            'fields': ('display_order', 'is_active', 'joined_date')
        }),
    )


class ProjectGalleryInline(admin.TabularInline):
    model = ProjectGallery
    extra = 1
    fields = ['image', 'caption', 'display_order']


@admin.register(WorkProject)
class WorkProjectAdmin(admin.ModelAdmin):
    list_display = ['title', 'category', 'project_status', 'start_date', 'is_featured', 'is_published', 'views_count']
    list_filter = ['category', 'project_status', 'is_featured', 'is_published']
    search_fields = ['title', 'description', 'location']
    prepopulated_fields = {'slug': ('title',)}
    readonly_fields = ['views_count', 'created_at', 'updated_at']
    inlines = [ProjectGalleryInline]
    fieldsets = (
        ('Basic Information', {
            'fields': ('title', 'slug', 'short_description', 'description', 'featured_image')
        }),
        ('Classification', {
            'fields': ('category', 'project_status', 'is_featured', 'is_published')
        }),
        ('Project Details', {
            'fields': ('start_date', 'end_date', 'location', 'beneficiaries_count', 'budget', 'partners')
        }),
        ('Statistics', {
            'fields': ('views_count', 'created_at', 'updated_at')
        }),
    )


@admin.register(MediaGallery)
class MediaGalleryAdmin(admin.ModelAdmin):
    list_display = ['title', 'media_type', 'category', 'event_date', 'is_featured', 'uploaded_at']
    list_filter = ['media_type', 'category', 'is_featured', 'event_date']
    search_fields = ['title', 'caption']
    readonly_fields = ['uploaded_at', 'uploaded_by']
    fieldsets = (
        ('Media Information', {
            'fields': ('title', 'media_type', 'image', 'video_url', 'caption')
        }),
        ('Classification', {
            'fields': ('category', 'event_date', 'is_featured', 'display_order')
        }),
        ('Metadata', {
            'fields': ('uploaded_at', 'uploaded_by')
        }),
    )
    
    def save_model(self, request, obj, form, change):
        if not obj.uploaded_by:
            obj.uploaded_by = request.user
        super().save_model(request, obj, form, change)


@admin.register(SiteSettings)
class SiteSettingsAdmin(admin.ModelAdmin):
    fieldsets = (
        ('About Section', {
            'fields': ('about_overview', 'mission_statement', 'vision_statement', 'achievements_summary')
        }),
        ('Statistics', {
            'fields': ('total_beneficiaries', 'total_projects', 'established_year', 'registration_number')
        }),
        ('Homepage Content', {
            'fields': ('homepage_hero_title', 'homepage_hero_subtitle', 'donation_appeal_text', 'volunteer_appeal_text')
        }),
        ('Contact & Social', {
            'fields': ('contact_email', 'contact_phone', 'contact_address', 'social_media_links')
        }),
        ('Payment', {
            'fields': ('donation_upi_vpa',)
        }),
        ('Footer', {
            'fields': ('footer_about_text',)
        }),
        ('SEO', {
            'fields': ('meta_description', 'meta_keywords')
        }),
    )
    
    def has_add_permission(self, request):
        return False
    
    def has_delete_permission(self, request, obj=None):
        return False


@admin.register(SliderImage)
class SliderImageAdmin(admin.ModelAdmin):
    list_display = ['title', 'display_order', 'is_active', 'uploaded_at']
    list_filter = ['is_active', 'uploaded_at']
    search_fields = ['title', 'caption']
    readonly_fields = ['uploaded_at']
    fieldsets = (
        ('Image Information', {
            'fields': ('title', 'image', 'caption')
        }),
        ('Display Settings', {
            'fields': ('display_order', 'is_active', 'link_url')
        }),
        ('Metadata', {
            'fields': ('uploaded_at',)
        }),
    )
    ordering = ['display_order', 'uploaded_at']


@admin.register(SiteStatistics)
class SiteStatisticsAdmin(admin.ModelAdmin):
    fieldsets = (
        ('Statistics', {
            'fields': ('total_beneficiaries', 'completed_projects', 'years_of_service', 'total_volunteers', 'total_donations')
        }),
    )
    
    def has_add_permission(self, request):
        return False
    
    def has_delete_permission(self, request, obj=None):
        return False
