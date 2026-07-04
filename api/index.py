import sys
import os
from pathlib import Path

# Set up the Django environment
BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(BASE_DIR))
sys.path.insert(0, str(BASE_DIR / 'myproject'))

# Set Django settings module
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'myproject.settings')

# Setup Django
import django
from django.conf import settings

# Configure for Vercel before Django setup
os.environ['DEBUG'] = 'False'

django.setup()

from django.core.wsgi import get_wsgi_application

# Override ALLOWED_HOSTS for Vercel
if 'VERCEL' in os.environ or 'VERCEL_URL' in os.environ:
    settings.ALLOWED_HOSTS = ['*']
    settings.DEBUG = False
    # Set CSRF trusted origins
    vercel_url = os.environ.get('VERCEL_URL', '')
    if vercel_url:
        settings.CSRF_TRUSTED_ORIGINS = [f'https://{vercel_url}', f'http://{vercel_url}']

# Create WSGI application
app = get_wsgi_application()





