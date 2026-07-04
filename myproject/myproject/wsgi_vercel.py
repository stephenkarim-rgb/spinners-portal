import os
import sys
from pathlib import Path

# Add the project directory to the Python path
BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(BASE_DIR))

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'myproject.settings')

import django
django.setup()

from django.core.wsgi import get_wsgi_application
from django.conf import settings

# Disable some warnings in production
if not settings.DEBUG:
    import warnings
    warnings.filterwarnings('ignore')

application = get_wsgi_application()
