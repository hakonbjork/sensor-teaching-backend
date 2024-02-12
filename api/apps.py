from django.apps import AppConfig


class ApiConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "api"

    def ready(self) -> None:
        """ This will be called when the app is ready. It runs once on statup."""
        from . import startup
        startup.init_backend()
        return super().ready()
