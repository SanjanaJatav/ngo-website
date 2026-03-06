"""
Management command to seed database with sample data for development
"""
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from main.models import (
    SiteSettings, TeamMember, WorkProject, MediaGallery,
    Donation, Volunteer, ContactSubmission
)
from django.utils import timezone
from datetime import timedelta
import random


class Command(BaseCommand):
    help = 'Seed the database with sample data for development'

    def handle(self, *args, **kwargs):
        self.stdout.write('Seeding database...')

        # Create Site Settings
        settings, _ = SiteSettings.objects.get_or_create(pk=1)
        settings.about_overview = (
            "Shree Brijwasi Jatav Samaj Sewa Samiti is a registered non-profit organization "
            "dedicated to uplifting marginalized communities through education, healthcare, "
            "and sustainable development. Founded with a vision to create an equitable society, "
            "we have been working tirelessly to bridge the gap between privilege and poverty. "
            "Our comprehensive programs span across education scholarships, medical camps, "
            "skill development workshops, women empowerment initiatives, and environmental "
            "conservation projects. We believe in the power of collective action and community-driven change."
        )
        settings.mission_statement = (
            "To empower underprivileged communities through quality education, accessible healthcare, "
            "and sustainable livelihood opportunities, ensuring dignity and equality for all. "
            "We strive to create an inclusive society where every individual can realize their full potential."
        )
        settings.vision_statement = (
            "A just and equitable society where every individual, regardless of their background, "
            "has access to education, healthcare, and opportunities for growth. We envision communities "
            "that are self-reliant, empowered, and living with dignity."
        )
        settings.achievements_summary = (
            "Over the years, we have impacted thousands of lives through our various programs. "
            "From providing scholarships to over 500 students to conducting 50+ medical camps, "
            "our commitment to social empowerment continues to grow."
        )
        settings.total_beneficiaries = 15000
        settings.total_projects = 47
        settings.established_year = 2015
        settings.registration_number = 'REG/NGO/2015/DL/12345'
        settings.homepage_hero_title = 'Shree Brijwasi Jatav Samaj Sewa Samiti'
        settings.homepage_hero_subtitle = 'Journey of Empowerment and Impact'
        settings.donation_appeal_text = (
            "Your generous contribution enables us to continue transforming lives. "
            "Every rupee you donate goes directly towards education, healthcare, and "
            "community development programs. Together, we can create lasting change."
        )
        settings.volunteer_appeal_text = (
            "Join our passionate team of volunteers and be part of something meaningful. "
            "Whether you can contribute a few hours a week or dedicate more time, "
            "your skills and enthusiasm can make a real difference in someone's life."
        )
        settings.footer_about_text = (
            "Shree Brijwasi Jatav Samaj Sewa Samiti is a dedicated NGO working towards "
            "social empowerment and community service since 2015. We believe in the power "
            "of collective action to create lasting positive change."
        )
        settings.meta_description = (
            "Shree Brijwasi Jatav Samaj Sewa Samiti - A dedicated NGO empowering communities "
            "through education, healthcare, and sustainable development."
        )
        settings.meta_keywords = (
            "NGO, social service, community empowerment, education, healthcare, "
            "volunteer, donation, Brijwasi, Jatav, Samaj Sewa"
        )
        settings.save()
        self.stdout.write(self.style.SUCCESS('[OK] Site Settings created'))

        # Create Team Members
        team_data = [
            {
                'name': 'Rajesh Kumar Jatav',
                'position': 'President & Founder',
                'bio': 'A visionary leader with over 20 years of experience in social work and community development. Rajesh founded the organization with a dream to uplift marginalized communities and has led numerous successful initiatives in education and healthcare.',
                'display_order': 1,
            },
            {
                'name': 'Sunita Devi',
                'position': 'Vice President',
                'bio': 'A passionate advocate for women\'s rights and education. Sunita has been instrumental in launching women empowerment programs and has helped hundreds of women gain financial independence through skill development.',
                'display_order': 2,
            },
            {
                'name': 'Amit Verma',
                'position': 'General Secretary',
                'bio': 'A dedicated social worker with a background in public administration. Amit oversees the day-to-day operations of the organization and ensures all programs run efficiently and effectively.',
                'display_order': 3,
            },
            {
                'name': 'Priya Sharma',
                'position': 'Treasurer',
                'bio': 'A chartered accountant by profession, Priya manages the financial operations of the NGO with utmost transparency. She ensures every donation is utilized effectively for the intended cause.',
                'display_order': 4,
            },
            {
                'name': 'Dr. Manoj Kumar',
                'position': 'Health Program Director',
                'bio': 'A medical professional committed to making healthcare accessible to all. Dr. Manoj leads our health camps and medical outreach programs across rural areas.',
                'display_order': 5,
            },
            {
                'name': 'Kavita Jatav',
                'position': 'Education Program Head',
                'bio': 'With a Master\'s in Education, Kavita designs and implements our educational programs. She has helped establish study centres in underserved areas and manages our scholarship program.',
                'display_order': 6,
            },
        ]

        for data in team_data:
            TeamMember.objects.update_or_create(
                name=data['name'],
                defaults=data
            )
        self.stdout.write(self.style.SUCCESS(f'[OK] {len(team_data)} Team Members created'))

        # Create Work Projects
        projects_data = [
            {
                'title': 'Education for All Initiative',
                'description': 'A comprehensive education program providing scholarships, study materials, and mentoring to underprivileged children. We have established 5 study centres across Delhi and surrounding areas, serving over 500 students annually. The program includes after-school tutoring, career counseling, and computer literacy training.',
                'short_description': 'Providing quality education and scholarships to underprivileged children across Delhi-NCR region.',
                'category': 'education',
                'project_status': 'ongoing',
                'start_date': timezone.now().date() - timedelta(days=730),
                'location': 'Delhi-NCR Region',
                'beneficiaries_count': 2500,
                'is_featured': True,
                'is_published': True,
            },
            {
                'title': 'Rural Health Camp Program',
                'description': 'Regular medical camps in rural areas providing free health checkups, medicines, and health awareness sessions. Our team of volunteer doctors and healthcare professionals conduct camps monthly, focusing on preventive healthcare, maternal health, and chronic disease management.',
                'short_description': 'Free medical camps providing healthcare access to underserved rural communities.',
                'category': 'health',
                'project_status': 'ongoing',
                'start_date': timezone.now().date() - timedelta(days=365),
                'location': 'Haryana & Rajasthan Villages',
                'beneficiaries_count': 5000,
                'is_featured': True,
                'is_published': True,
            },
            {
                'title': 'Women Empowerment Workshop',
                'description': 'Skill development workshops for women covering tailoring, handicrafts, computer basics, and financial literacy. The program aims to make women financially independent by providing vocational training and connecting them with market opportunities.',
                'short_description': 'Empowering women through skill development, vocational training, and financial literacy programs.',
                'category': 'women_empowerment',
                'project_status': 'ongoing',
                'start_date': timezone.now().date() - timedelta(days=540),
                'location': 'New Delhi',
                'beneficiaries_count': 800,
                'is_featured': True,
                'is_published': True,
            },
            {
                'title': 'Clean Village Campaign',
                'description': 'An environmental initiative focused on waste management, tree plantation, and sanitation awareness in rural villages. We have planted over 10,000 trees and installed waste segregation systems in 20 villages.',
                'short_description': 'Environmental conservation through tree plantation, waste management, and sanitation awareness.',
                'category': 'environment',
                'project_status': 'completed',
                'start_date': timezone.now().date() - timedelta(days=900),
                'end_date': timezone.now().date() - timedelta(days=180),
                'location': 'Uttar Pradesh Villages',
                'beneficiaries_count': 3000,
                'is_featured': False,
                'is_published': True,
            },
            {
                'title': 'Child Nutrition Program',
                'description': 'Addressing malnutrition among children in urban slums through mid-day meal programs, nutrition awareness sessions, and supplementary feeding. We provide balanced meals to over 200 children daily.',
                'short_description': 'Combating child malnutrition through daily meal programs and nutrition awareness in urban slums.',
                'category': 'child_welfare',
                'project_status': 'ongoing',
                'start_date': timezone.now().date() - timedelta(days=450),
                'location': 'Delhi Slum Areas',
                'beneficiaries_count': 1200,
                'is_featured': False,
                'is_published': True,
            },
            {
                'title': 'Community Library Network',
                'description': 'Establishing community libraries in underserved areas to promote reading habits and provide access to educational resources. Each library is equipped with books, computers, and internet access.',
                'short_description': 'Building community libraries with books, computers, and internet in underserved neighbourhoods.',
                'category': 'community',
                'project_status': 'completed',
                'start_date': timezone.now().date() - timedelta(days=600),
                'end_date': timezone.now().date() - timedelta(days=90),
                'location': 'Multiple Locations, Delhi',
                'beneficiaries_count': 1500,
                'is_featured': False,
                'is_published': True,
            },
        ]

        for data in projects_data:
            WorkProject.objects.update_or_create(
                title=data['title'],
                defaults=data
            )
        self.stdout.write(self.style.SUCCESS(f'[OK] {len(projects_data)} Work Projects created'))

        # Create Media Gallery items
        media_data = [
            {'title': 'Annual Day Celebration 2025', 'media_type': 'image', 'category': 'events', 'is_featured': True},
            {'title': 'Health Camp in Faridabad', 'media_type': 'image', 'category': 'activities', 'is_featured': True},
            {'title': 'Women Empowerment Workshop', 'media_type': 'image', 'category': 'workshops', 'is_featured': False},
            {'title': 'Education Award Ceremony', 'media_type': 'image', 'category': 'achievements', 'is_featured': True},
            {'title': 'Tree Plantation Drive', 'media_type': 'image', 'category': 'activities', 'is_featured': False},
            {'title': 'Community Library Opening', 'media_type': 'image', 'category': 'events', 'is_featured': False},
        ]

        for i, data in enumerate(media_data):
            data['event_date'] = timezone.now().date() - timedelta(days=random.randint(30, 365))
            data['display_order'] = i
            data['caption'] = f"Highlights from {data['title']}"
            MediaGallery.objects.update_or_create(
                title=data['title'],
                defaults=data
            )
        self.stdout.write(self.style.SUCCESS(f'[OK] {len(media_data)} Media Gallery items created'))

        self.stdout.write(self.style.SUCCESS('\nDatabase seeded successfully!'))
        self.stdout.write(self.style.SUCCESS('   Admin login: admin / admin123'))
        self.stdout.write(self.style.SUCCESS('   Run: python manage.py runserver'))
