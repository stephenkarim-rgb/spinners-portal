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
django.setup()

from django.core.wsgi import get_wsgi_application
from django.conf import settings

# Override some settings for Vercel
if 'VERCEL' in os.environ:
    settings.DEBUG = False
    settings.ALLOWED_HOSTS = ['*.vercel.app', 'localhost', '127.0.0.1']

# Create WSGI application
app = get_wsgi_application()




