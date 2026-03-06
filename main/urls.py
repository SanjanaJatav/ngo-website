"""
URL patterns for main app
"""

from django.urls import path
from . import views

urlpatterns = [
    path('', views.home_view, name='home'),
    path('about/overview/', views.about_overview_view, name='about_overview'),
    path('about/team/', views.team_view, name='team'),
    path('our-work/', views.our_work_view, name='our_work'),
    path('our-work/<slug:slug>/', views.project_detail_view, name='project_detail'),
    path('donate/', views.donate_view, name='donate'),
    path('donate/thank-you/', views.donation_thank_you_view, name='donation_thank_you'),
    path('media/', views.media_view, name='media'),
    path('contact/', views.contact_view, name='contact'),
    path('volunteer/', views.volunteer_view, name='volunteer'),
    path('volunteer/thank-you/', views.volunteer_thank_you_view, name='volunteer_thank_you'),
]
