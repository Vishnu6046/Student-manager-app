from django.shortcuts import redirect
from django.urls import reverse
from django.utils.deprecation import MiddlewareMixin

class RedirectAuthenticatedUserMiddleware(MiddlewareMixin):
    def process_request(self, request):
        if request.user.is_authenticated:
            login_urls = [
                reverse('student_login'),
                reverse('staff_login'),
                reverse('admin_login'),
            ]
            if request.path in login_urls:
                profile = getattr(request.user, 'profile', None)
                if profile:
                    if profile.user_type == 'student':
                        return redirect('student_home')
                    elif profile.user_type == 'staff':
                        return redirect('staff_home')
                    elif profile.user_type == 'admin':
                        return redirect('admin_home')

class NoCacheMiddleware(MiddlewareMixin):
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        response['Cache-Control'] = 'no-cache, no-store, must-revalidate'
        response['Pragma'] = 'no-cache'
        response['Expires'] = '0'
        return response