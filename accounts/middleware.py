from django.shortcuts import redirect
from django.urls import reverse, NoReverseMatch

EXEMPT_PATHS = [
    '/admin/login/',
]

def safe_reverse(name):
    try:
        return reverse(name)
    except NoReverseMatch:
        return None

class ForcePasswordChangeMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        user = getattr(request, 'user', None)

        if user and user.is_authenticated:
            change_url = safe_reverse('change_password')
            logout_url = safe_reverse('logout')
            login_url = safe_reverse('login')
            refresh_url = safe_reverse('token_refresh')

            exempt = [u for u in [change_url, logout_url, login_url, refresh_url] if u] + EXEMPT_PATHS

            if user.must_change_password and request.path != change_url and not any(request.path.startswith(path) for path in exempt):
                return redirect(change_url)

        return self.get_response(request)

