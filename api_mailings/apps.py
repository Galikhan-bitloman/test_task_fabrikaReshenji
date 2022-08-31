from django.apps import AppConfig


class ApiMailingsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'api_mailings'

    def ready(self):
        from api_mailings import signals
