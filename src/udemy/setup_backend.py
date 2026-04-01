#!/usr/bin/env python
"""
Backend Setup Script for Udemy Learning Platform
This script helps set up the Django backend with proper migrations and initial data.
"""

import os
import sys
import django
from django.core.management import execute_from_command_line
from django.contrib.auth.models import User
from courses.models import MainCategory, SubCategory, Course, Video
from datetime import timedelta

def setup_django():
    """Setup Django environment"""
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'udemy.settings')
    django.setup()

def run_migrations():
    """Run Django migrations"""
    print("Running migrations...")
    execute_from_command_line(['manage.py', 'makemigrations'])
    execute_from_command_line(['manage.py', 'migrate'])
    print("Migrations completed successfully!")

def create_superuser():
    """Create a superuser if none exists"""
    if not User.objects.filter(is_superuser=True).exists():
        print("Creating superuser...")
        User.objects.create_superuser(
            username='admin',
            email='admin@example.com',
            password='admin123'
        )
        print("Superuser created: admin/admin123")
    else:
        print("Superuser already exists")

def create_sample_data():
    """Create sample categories and courses"""
    print("Creating sample data...")
    
    # Create main categories
    development = MainCategory.objects.get_or_create(
        name='Development',
        slug='development'
    )[0]
    
    business = MainCategory.objects.get_or_create(
        name='Business',
        slug='business'
    )[0]
    
    design = MainCategory.objects.get_or_create(
        name='Design',
        slug='design'
    )[0]
    
    # Create subcategories
    web_dev = SubCategory.objects.get_or_create(
        main_category=development,
        name='Web Development',
        slug='web-development',
        learners_count='50,000+'
    )[0]
    
    python_dev = SubCategory.objects.get_or_create(
        main_category=development,
        name='Python Programming',
        slug='python-programming',
        learners_count='30,000+'
    )[0]
    
    # Create sample courses
    if not Course.objects.exists():
        course1 = Course.objects.create(
            sub_category=web_dev,
            title='Complete Web Development Bootcamp',
            description='Learn web development from scratch with HTML, CSS, JavaScript, and more.',
            price=999,
            rating_point='4.5',
            reviews='150',
            created_by='John Doe',
            premium=True,
            best_seller=True
        )
        
        course2 = Course.objects.create(
            sub_category=python_dev,
            title='Python for Beginners',
            description='Master Python programming fundamentals and build real-world projects.',
            price=799,
            rating_point='4.8',
            reviews='200',
            created_by='Jane Smith',
            premium=False,
            best_seller=True
        )
        
        # Create sample videos
        Video.objects.create(
            course=course1,
            title='Introduction to HTML',
            description='Learn the basics of HTML markup',
            duration=timedelta(minutes=15),
            order=1,
            is_preview=True
        )
        
        Video.objects.create(
            course=course1,
            title='CSS Fundamentals',
            description='Style your web pages with CSS',
            duration=timedelta(minutes=20),
            order=2,
            is_preview=False
        )
        
        Video.objects.create(
            course=course2,
            title='Python Basics',
            description='Introduction to Python programming',
            duration=timedelta(minutes=25),
            order=1,
            is_preview=True
        )
        
        print("Sample data created successfully!")
    else:
        print("Sample data already exists")

def main():
    """Main setup function"""
    print("🚀 Setting up Udemy Learning Platform Backend...")
    
    try:
        setup_django()
        run_migrations()
        create_superuser()
        create_sample_data()
        
        print("\n✅ Backend setup completed successfully!")
        print("\n📋 Next steps:")
        print("1. Install dependencies: pip install -r requirements.txt")
        print("2. Run the server: python manage.py runserver")
        print("3. Access admin panel: http://localhost:8000/admin/")
        print("4. API documentation: Check API_ENDPOINTS.md")
        print("\n🔑 Admin credentials: admin/admin123")
        
    except Exception as e:
        print(f"❌ Setup failed: {str(e)}")
        sys.exit(1)

if __name__ == '__main__':
    main() 