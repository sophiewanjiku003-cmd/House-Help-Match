#!/usr/bin/env python
"""
Test script to verify Gmail email configuration
Run: python test_email_config.py
"""
import os
import sys
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.core.mail import send_mail
from django.conf import settings

print("=" * 60)
print("TESTING GMAIL EMAIL CONFIGURATION")
print("=" * 60)

print(f"\n📧 Email Settings:")
print(f"  EMAIL_BACKEND: {settings.EMAIL_BACKEND}")
print(f"  EMAIL_HOST: {settings.EMAIL_HOST}")
print(f"  EMAIL_PORT: {settings.EMAIL_PORT}")
print(f"  EMAIL_USE_TLS: {settings.EMAIL_USE_TLS}")
print(f"  EMAIL_HOST_USER: {settings.EMAIL_HOST_USER}")
print(f"  DEFAULT_FROM_EMAIL: {settings.DEFAULT_FROM_EMAIL}")

print(f"\n🔄 Attempting to send test email...")

try:
    result = send_mail(
        subject='House-Help Password Reset Test',
        message='This is a test email from your House-Help deployment. If you received this, email is working!',
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=['blaisengugi3@gmail.com'],
        fail_silently=False,
    )
    
    if result == 1:
        print("✅ SUCCESS! Test email sent successfully!")
        print("\nEmail should arrive in: blaisengugi3@gmail.com inbox")
        print("\nPassword reset feature is working! Users can:")
        print("  1. Click 'Forgot Password' on login page")
        print("  2. Enter their email address")
        print("  3. Receive password reset link via email")
        print("  4. Set new password")
    else:
        print("⚠️  Email returned 0 - may have failed silently")
        
except Exception as e:
    print(f"❌ ERROR: {str(e)}")
    print("\nTroubleshooting:")
    print("  1. Check .env file has correct Gmail credentials")
    print("  2. If using Gmail password: Enable 'Less secure apps'")
    print("  3. If using Gmail App Password: Generate from Account Settings")
    print("  4. Verify internet connection")
    
print("\n" + "=" * 60)
