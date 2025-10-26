from django.apps import AppConfig


class CrmnewConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'crmnew'
    def ready(self):
       import crmnew.signals
