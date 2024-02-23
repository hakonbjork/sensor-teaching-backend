from . import util

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