# middleware.py
from django.shortcuts import redirect
from django.urls import reverse
from django.conf import settings

EXEMPT_PATHS = [
    '/admin/login/',  # if you want to allow admin login page
]

class ForcePasswordChangeMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Only run for authenticated users
        user = getattr(request, 'user', None)
        if user and user.is_authenticated:
            # Do nothing if already changing password or logging out, or if it's an exempt path
            change_url = reverse('change_password')
            logout_url = reverse('logout') if 'logout' in [u.name for u in getattr(settings, 'ROOT_URLCONF', [])] else None
            exempt = [change_url, getattr(logout_url, 'pattern', '')] + EXEMPT_PATHS

            if user.must_change_password and request.path != change_url and not any(request.path.startswith(p) for p in exempt):
                # If the request is not the change-password endpoint, redirect them there
                return redirect(change_url)

        return self.get_response(request)
