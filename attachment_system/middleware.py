from django.http import HttpResponseForbidden
from .models import SystemControl

class SystemLockdownMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Allow Admin path access and Superusers to stay active to open/close system
        if not request.path.startswith('/admin'):
            if not request.user.is_superuser:
                sys_control = SystemControl.objects.first()
                if sys_control and sys_control.is_system_closed:
                    return HttpResponseForbidden("<h1>System busy, try again later.</h1>")
        
        return self.get_response(request)