# Ensure your app is registered
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'attachment_system', # Your custom app
]

# Point Django to use our modified Custom User Identity model
AUTH_USER_MODEL = 'attachment_system.CompanyUser'

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    # Register the System Lockout Interceptor
    'attachment_system.middleware.SystemLockdownMiddleware', 
]

# File upload specifications
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# Configuration for test emails (prints OTPs directly to terminal window)
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'