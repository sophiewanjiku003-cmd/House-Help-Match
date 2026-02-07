import os
import sys
import django

# Ensure project root is on sys.path when running from scripts/
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, project_root)

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.contrib.auth import get_user_model
User = get_user_model()

username = 'ADMIN'
email = 'admin@example.com'
password = 'Admin12345'

user = User.objects.filter(username=username).first()
if user:
    user.set_password(password)
    user.is_staff = True
    user.is_superuser = True
    user.save()
    print('UPDATED', username)
else:
    User.objects.create_superuser(username=username, email=email, password=password)
    print('CREATED', username)

print('NOTE: Password set as requested but not echoed for security.')
