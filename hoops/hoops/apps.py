from django.apps import AppConfig


class HoopsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'hoops'

    def ready(self):
        import hoops.signals