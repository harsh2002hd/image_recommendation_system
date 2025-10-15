import os
import sys
import django
from django.contrib.auth import get_user_model

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'img_recommendation_system.settings')
sys.path.append(os.getcwd())
django.setup()

# Get the User model
User = get_user_model()

# Create a superuser
username = 'admin'
email = 'admin@example.com'
password = 'admin123'

try:
    user = User.objects.create_superuser(username, email, password)
    print(f'Superuser "{username}" created successfully!')
    print(f'Username: {username}')
    print(f'Password: {password}')
    print('Please change this password after your first login.')
except Exception as e:
    print(f'Error creating superuser: {e}')