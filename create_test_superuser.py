#!/usr/bin/env python
"""
Quick script to create a superuser for testing
Run: python create_test_superuser.py
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.contrib.auth.models import User

# Check if admin already exists
if not User.objects.filter(username='admin').exists():
    User.objects.create_superuser(
        username='admin',
        email='blaisengugi3@gmail.com',
        password='Admin123!'
    )
    print("✅ Superuser 'admin' created successfully!")
    print("\nLogin credentials:")
    print("  Username: admin")
    print("  Email: blaisengugi3@gmail.com")
    print("  Password: Admin123!")
    print("\nAccess admin at: http://localhost:8000/admin/")
else:
    print("⚠️  Superuser 'admin' already exists")
