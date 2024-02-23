import time
import os
import csv
from dataprocessing import util


def compute_emotion():
    """
    This function reads a frame from the webcam,
    finds the emotion from the PyEmotion package
    And writes it to it's csv file
    """
    import cv2 as cv
    import PyEmotion

    # wait for user settings to begin
    util.read_user_settings()

    # Open you default camera
    cap = cv.VideoCapture(0)
    cap.set(cv.CAP_PROP_BUFFERSIZE, 1)
    er = PyEmotion.DetectFace(device='cpu', gpu_id=0)
    while True:
        _, frame = cap.read()
        _, emotion = er.predict_emotion(frame)
        if emotion:
            _set_state_from_emotion(emotion.lower())
        # only find emotion once every second
        time.sleep(1)

def _set_state_from_emotion(new_emotion):
    """ Set the new emotion to True and the rest to False. """
    emotions = {"neutral": False, "angry": False, "fear": False, "happy": False, "sad": False, "surprise": False, "disgust": False}
    for e in emotions.keys():
        emotions[e] = False
    emotions[new_emotion] = True
    _write_emotions_to_csv(emotions)

def _write_emotions_to_csv(emotions):
        filepath = 'data/emotions.csv'
        file_exists = os.path.exists(filepath) and os.path.getsize(filepath) > 0
        timestamp = time.time()
        emotions_with_timestamp = {"timestamp": timestamp}
        emotions_with_timestamp.update(emotions)

        with open(filepath, 'a', newline='') as csvfile:
            fieldnames = ['timestamp'] + list(emotions.keys())
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

            # Write the header only if the file did not exist or was empty
            if not file_exists:
                writer.writeheader()

            # Write the updated emotions as a new row
            writer.writerow(emotions_with_timestamp)
