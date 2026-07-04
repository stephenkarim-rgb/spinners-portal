import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'myproject.settings')
django.setup()

from attachment_system.models import CompanyUser

# Create or update the admin user
user, created = CompanyUser.objects.get_or_create(
    username='SPINNERS',
    defaults={
        'email': 'solutions@spinners.co.ke',
        'first_name': 'Admin',
        'is_staff': True,
        'is_superuser': True,
    }
)

# Delete old 'solutions' user if it exists
try:
    old_user = CompanyUser.objects.get(username='solutions')
    old_user.delete()
    print("Old 'solutions' user deleted")
except CompanyUser.DoesNotExist:
    pass

# Update user
user.email = 'solutions@spinners.co.ke'
user.is_staff = True
user.is_superuser = True
user.set_password('Spinners@12k$')
user.save()

print(f"Admin user updated: {user.username} ({user.email})")
print(f"Login with:")
print(f"  Username: SPINNERS")
print(f"  Password: Spinners@12k$")
