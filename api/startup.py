from .empatica import EmpaticaConnection
from dataprocessing.handler import DataHandler
from dataprocessing.measurements import (compute_arousal, compute_engagement, compute_emotional_regulation, compute_entertainment, compute_stress)

def init_backend():
    """ Connects to empatica and starts the master backend"""

    print("starting master backend...")
    connection = EmpaticaConnection()

    # Instantiate the arousal data handler and subscribe to the api
    arousal_handler = DataHandler(
        measurement_func=compute_arousal,
        measurement_path="arousal.csv",
        window_length=121,
        window_step=40,
        baseline_length=161
    )
    connection.add_subscriber(arousal_handler, "EDA")

    # Instantiate the engagement data handler and subscribe to the api
    engagement_handler = DataHandler(
        measurement_func=compute_engagement,
        measurement_path="engagement.csv",
        window_length=121,
        window_step=40,
        baseline_length=161,
        header_features=["amplitude", "nr of peaks", "area under curve of tonic signal"]
    )
    connection.add_subscriber(engagement_handler, "EDA")

    # Instantiate the emotional regulation data handler and subscribe to the api
    emreg_handler = DataHandler(
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
        measurement_func=compute_stress,
        measurement_path="stress.csv",
        window_length=10,
        window_step=10,
        baseline_length=30
    )
    connection.add_subscriber(stress_handler, "TEMP")

    connection.connect()