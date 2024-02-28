from .empatica import EmpaticaConnection
from dataprocessing.handler import DataHandler
from dataprocessing.measurements import (compute_arousal, compute_engagement, compute_emotional_regulation, compute_entertainment, compute_stress)
from dataprocessing.util import read_user_settings
from dataprocessing.firebase import init_firebase

started = False
    
def init_empatica(id):
    """ Connects to empatica and begnins the measurements """

    global started

    # blocks the thread until we have user settings
    print("Empatica: waiting for user settings...")
    user_settings = read_user_settings()
    if user_settings["empatica-used"].lower() != "true":
        print("Empatica not in use, skipping empatica measurements")
        return
    
    id_mapping = {
        1: "904ACD",
        2: "D631CD"
    }

    user_id_left = user_settings["id_left"]
    user_id_right = user_settings["id_right"]

    # change this later to use actual id or something,
    # for now only uses number from apps.py and the two devices we have
    device_id = id_mapping[id]
    
    init_firebase()

    if started:
        return
    print("starting empatica measurements...")
    connection = EmpaticaConnection()
    started = True

    # Instantiate the arousal data handler and subscribe to the api
    arousal_handler = DataHandler(
        id=user_id_left,
        measurement_func=compute_arousal,
        measurement_path="arousal.csv",
        window_length=121,
        window_step=40,
        baseline_length=161
    )
    connection.add_subscriber(arousal_handler, "EDA")

    # Instantiate the engagement data handler and subscribe to the api
    engagement_handler = DataHandler(
        id=user_id_left if id == 1 else user_id_right,
        measurement_func=compute_engagement,
        measurement_path="engagement.csv",
        measurement_type="engagement",
        window_length=121,
        window_step=40,
        baseline_length=161,
        header_features=["amplitude", "nr of peaks", "area under curve of tonic signal"]
    )
    connection.add_subscriber(engagement_handler, "EDA")

    # Instantiate the emotional regulation data handler and subscribe to the api
    emreg_handler = DataHandler(
        id=user_id_left,
        measurement_func=compute_emotional_regulation,
        measurement_path="emotional_regulation.csv",
        window_length=12,
        window_step=12,
        baseline_length=36,
        header_features=["rmssd", "outliers", "mean"]
    )
    connection.add_subscriber(emreg_handler, "IBI")

    # Instantiate the entertainment data handler and subscribe to the api
    entertainment_handler = DataHandler(
        id=user_id_left,
        measurement_func=compute_entertainment,
        measurement_path="entertainment.csv",
        window_length=20,
        window_step=10,
        baseline_length=30,
        header_features=["mean", "var", "max", "min", "diff", "correlation",
                         "auto-correlation", "approximate entropy", "fluctuations"]
    )
    connection.add_subscriber(entertainment_handler, "HR")

    # Instantiate the stress data handler and subscribe to the api
    stress_handler = DataHandler(
        id=user_id_left if id == 1 else user_id_right,
        measurement_func=compute_stress,
        measurement_path="stress.csv",
        measurement_type="stress",
        window_length=10,
        window_step=10,
        baseline_length=30
    )
    connection.add_subscriber(stress_handler, "TEMP")

    connection.connect(device_id)