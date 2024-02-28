import time
import os
import csv
from dataprocessing import util, firebase

DEFAULT_EMOTIONS = {"neutral": False, "angry": False, "fear": False, "happy": False, "sad": False, "surprise": False, "disgust": False}

def compute_emotion():
    """
    This function reads a frame from the webcam,
    finds the emotion from the PyEmotion package
    And writes it to it's csv file
    """
    import cv2 as cv
    import PyEmotion

    # wait for user settings to begin
    print("Emotions: waiting for user settings...")
    user_settings = util.read_user_settings()
    print("Emotions: user settings found")
    user_id = user_settings["id"]

    # Open you default camera
    cap = cv.VideoCapture(0)
    cap.set(cv.CAP_PROP_BUFFERSIZE, 1)
    er = PyEmotion.DetectFace(device='cpu', gpu_id=0)
    firebase.init_firebase()
    while True:
        _, frame = cap.read()
        _, emotions = er.predict_emotion(frame)
        _set_state_from_emotion(user_id, emotions)
        # only find emotion once every second
        time.sleep(1)

def _set_state_from_emotion(id, new_emotions):
    """ Set the new emotion to True and the rest to False. """
    if (new_emotions) == "noface": # no face detected
         return
    
    if len(new_emotions) > 1: # several faces detected
        left_emotion = new_emotions[0].lower()
        right_emotion = new_emotions[1].lower()
        left_emotion_dict = _compute_emotions_dict(left_emotion)
        right_emotion_dict = _compute_emotions_dict(right_emotion)
        _write_emotions_to_csv([left_emotion_dict, right_emotion_dict], 1, 2)
        firebase.add_data(1, left_emotion_dict)
        firebase.add_data(2, right_emotion_dict)
    
    else: # only one face detected
        emotion = new_emotions[0].lower()
        emotion_dict = _compute_emotions_dict(emotion)
        firebase.add_data(id, emotion_dict)
        _write_emotions_to_csv([emotion_dict], 1)
        
def _compute_emotions_dict(current_emotion):
    emotions = DEFAULT_EMOTIONS
    for e in emotions.keys():
        emotions[e] = False
    emotions[current_emotion] = True
    return emotions

def _write_emotions_to_csv(emotions, id1, id2=None):
        filepath_base = 'data/emotions'
        filepath_end = '.csv'
        timestamp = time.time()
        ids = [id1, id2]

        for i in range(len(emotions)):
            if i > 1: break # we always have max two emotions
            if i > 0 and id2 is None: break # if we only have one id, we can't write two emotions

            path = f"{filepath_base}_{ids[i]}{filepath_end}" # file name is based on the user id
            file_exists = os.path.exists(path) and os.path.getsize(path) > 0
            emotions_with_timestamp = {"timestamp": timestamp}
            emotion_dict = emotions[i]
            emotions_with_timestamp.update(emotion_dict)

            with open(path, 'a', newline='') as csvfile:
                fieldnames = ['timestamp'] + list(DEFAULT_EMOTIONS.keys())
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

                # Write the header only if the file did not exist or was empty
                if not file_exists:
                    writer.writeheader()

                # Write the updated emotions as a new row
                writer.writerow(emotions_with_timestamp)
