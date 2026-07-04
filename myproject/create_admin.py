import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'myproject.settings')
django.setup()

from attachment_system.models import CompanyUser

# Create or update the admin user
user, created = CompanyUser.objects.get_or_create(
    username='solutions',
    defaults={
        'email': 'solutions@spinners.co.ke',
        'first_name': 'Admin',
        'is_staff': True,
        'is_superuser': True,
    }
)

if not created:
    user.email = 'solutions@spinners.co.ke'
    user.is_staff = True
    user.is_superuser = True
    user.save()

# Set password
user.set_password('solutions@spinners.co.ke')
user.save()

print(f"Admin user created/updated: {user.username} ({user.email})")
print(f"Login with:")
print(f"  Username: solutions")
print(f"  Email: solutions@spinners.co.ke")
print(f"  Password: solutions@spinners.co.ke")
