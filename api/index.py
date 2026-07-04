import sys
import os
from pathlib import Path

# Set up the Django environment
BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(BASE_DIR))
sys.path.insert(0, str(BASE_DIR / 'myproject'))

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'myproject.settings')

import django
django.setup()

from django.core.wsgi import get_wsgi_application
from django.conf import settings

# Ensure DEBUG is False in production
if 'VERCEL' in os.environ:
    settings.DEBUG = False

application = get_wsgi_application()



