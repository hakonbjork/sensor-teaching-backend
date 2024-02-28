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
        p1 = Process(target=compute_emotion)
        p1.start()

        p2 = Process(target=init_empatica, args=(1,))
        p2.start()

        p3 = Process(target=init_empatica, args=(2,))
        p3.start()
        
        return super().ready()
