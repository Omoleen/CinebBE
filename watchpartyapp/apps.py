from django.apps import AppConfig


class WatchpartyappConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'watchpartyapp'

    def ready(self):
        import watchpartyapp.signals
