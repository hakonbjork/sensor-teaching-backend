import csv
import os

# from camera we can get neutral, angry, fear, happy, sad, surprise, disgust (?)

class MeasurementStates:
    """ This class is responsible for keeping track of the states of the measurements. """

    SWITCH_POINT = 1

    # initial states starts with False
    _states = {
        "neutral": False,
        "angry": False,
        "fear": False,
        "happy": False,
        "sad": False,
        "surprise": False,
        "disgust": False,
        "engagement": False,
        "stress": False,
    }

    emotions = ["neutral", "angry", "fear", "happy", "sad", "surprise", "disgust"]

    @classmethod
    def set_state_from_normalized_measurement(cls, type, nm):
        cls._states[type] = float(nm) > cls.SWITCH_POINT
        MeasurementStates.write_state_to_csv()

    @classmethod
    def set_state_from_emotion(cls, emotion):
        # for e in cls.emotions:
        #     cls._states[e] = False
        cls._states[emotion] = True
        MeasurementStates.write_state_to_csv()
    
    @classmethod
    def write_state_to_csv(cls):
        filepath = 'data/states.csv'
        file_exists = os.path.exists(filepath) and os.path.getsize(filepath) > 0

        with open(filepath, 'a', newline='') as csvfile:
            fieldnames = list(cls._states.keys())
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

            # Write the header only if the file did not exist or was empty
            if not file_exists:
                writer.writeheader()

            # Write the updated states as a new row
            writer.writerow(cls._states)


    """ 
    In their frontend:
    (nm = normalized measurment)

    default = grey (C4C4C4)

    if nm > 1.25: red (F45656)
    else if nm > 1.15: orange (F4B556)
    else if nm > 0.85: grey (C4C4C4)
    else if nm > 0.75: light green (B3D2A0)
    else: green (8BD45F)

    Based on this, we propose setting 1 (middle of grey zone) as the "switch" point for yes/no

    """