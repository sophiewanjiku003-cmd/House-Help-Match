#!/usr/bin/env python
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.contrib.auth.models import User
from matchapp.models import UserProfile, JobCategory

# Create superuser
if not User.objects.filter(username='ADMIN').exists():
    user = User.objects.create_superuser('ADMIN', 'admin@househelp.com', 'Admin12345')
    UserProfile.objects.create(
        user=user,
        user_type='manager',
        phone='0123456789',
        address='Admin Office',
        city='Nairobi'
    )
    print("✓ Superuser created successfully")
else:
    print("✓ Superuser already exists")

# Create job categories
categories = [
    {'name': 'General Househelp', 'description': 'General housekeeping and cleaning services', 'icon': 'fas fa-home'},
    {'name': 'Cleaning & Housekeeping', 'description': 'Professional cleaning and house maintenance', 'icon': 'fas fa-broom'},
    {'name': 'Cooking & Kitchen', 'description': 'Food preparation and kitchen management', 'icon': 'fas fa-utensils'},
    {'name': 'Childcare', 'description': 'Child supervision and care services', 'icon': 'fas fa-child'},
    {'name': 'Elderly Care', 'description': 'Care for elderly and senior citizens', 'icon': 'fas fa-heart'},
    {'name': 'Pet Care', 'description': 'Pet grooming, walking, and care', 'icon': 'fas fa-paw'},
    {'name': 'Gardening & Landscaping', 'description': 'Garden maintenance and landscaping', 'icon': 'fas fa-leaf'},
    {'name': 'Laundry & Ironing', 'description': 'Laundry and ironing services', 'icon': 'fas fa-spray-can'},
    {'name': 'Babysitting', 'description': 'Professional babysitting services', 'icon': 'fas fa-baby'},
    {'name': 'Personal Assistant', 'description': 'Personal assistant and secretary services', 'icon': 'fas fa-tasks'},
]

created_count = 0
for cat in categories:
    obj, created = JobCategory.objects.get_or_create(
        name=cat['name'],
        defaults={
            'description': cat['description'],
            'icon': cat['icon']
        }
    )
    if created:
        created_count += 1

print(f"✓ Categories: {created_count} new categories created, {len(categories) - created_count} already existed")
print("\n✓ Database setup complete!")
