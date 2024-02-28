from django.apps import AppConfig
from multiprocessing import Process

class ApiConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "api"

    def ready(self) -> None:
        """ This will be called when the app is ready. It runs once on statup."""
        print("Starting application. This should only happen once")
        print("Waiting for user settings...")

        p0 = Process(target=_start_processes)
        p0.start()
        
        return super().ready()
    
def _start_processes():
    from .init_empatica import init_empatica
    from dataprocessing.measurements.emotion import compute_emotion
    from dataprocessing.util import read_user_settings

    user_settings = read_user_settings()
    print("User settings found")

    user_id_1 = user_settings["user_id_1"]
    user_id_2 = user_settings["user_id_2"]
    user_id_3 = user_settings["user_id_3"]

    ids = [user_id_1, user_id_2, user_id_3]

    group_size = 3 if user_id_3 != "" else 2

    p1 = Process(target=compute_emotion)
    p1.start()

    for i in range(group_size):
        p = Process(target=init_empatica, args=(ids[i],))
        p.start()
