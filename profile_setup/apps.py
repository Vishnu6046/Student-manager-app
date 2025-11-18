from django.apps import AppConfig


class ProfileSetupConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'profile_setup'

    def ready(self):
        import profile_setup.signals
