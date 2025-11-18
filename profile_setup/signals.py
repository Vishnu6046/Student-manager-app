from django.contrib.auth.signals import user_logged_in, user_logged_out
from django.contrib.sessions.models import Session
from django.dispatch import receiver
from django.contrib import messages
from django.contrib.auth import logout

@receiver(user_logged_out)
def clear_session_key(sender, request, user, **kwargs):
    if user:
        profile = getattr(user, 'profile', None)
        if profile:
            profile.session_key = None
            profile.save()
