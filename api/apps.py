from django.apps import AppConfig
from multiprocessing import Process

class ApiConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "api"

    def ready(self) -> None:
        """ This will be called when the app is ready. It runs once on statup."""
        print("Starting application. This should only happen once")

        from .init_empatica import init_empatica
        from dataprocessing.measurements.emotion import compute_emotion
        # p1 = Process(target=init_empatica)
        # p1.start()

        p2 = Process(target=compute_emotion)
        p2.start()
        
        return super().ready()
