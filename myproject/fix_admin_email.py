import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'myproject.settings')
django.setup()

from attachment_system.models import CompanyUser

# Find and update admin@example.com user
try:
    admin_user = CompanyUser.objects.get(email='admin@example.com')
    admin_user.email = 'solutions@spinners.co.ke'
    admin_user.username = 'SPINNERS'
    admin_user.set_password('Spinners@12k$')
    admin_user.is_staff = True
    admin_user.is_superuser = True
    admin_user.save()
    print(f"Updated admin user: {admin_user.username} ({admin_user.email})")
except CompanyUser.DoesNotExist:
    print("No user with admin@example.com found")

# Also make sure SPINNERS user exists and has correct settings
user, created = CompanyUser.objects.get_or_create(
    username='SPINNERS',
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
    user.set_password('Spinners@12k$')
    user.save()
    print(f"Updated SPINNERS user: {user.username} ({user.email})")
else:
    print(f"Created SPINNERS user: {user.username} ({user.email})")

# List all admin users
print("\nAll admin users:")
admins = CompanyUser.objects.filter(is_superuser=True)
for admin in admins:
    print(f"  - {admin.username} ({admin.email})")
