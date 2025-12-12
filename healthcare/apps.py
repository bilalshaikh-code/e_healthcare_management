from django.apps import AppConfig

class HealthCareConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'healthcare'

    def ready(self):
        import healthcare.signals  # This loads the signals
