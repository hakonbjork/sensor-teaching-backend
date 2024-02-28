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
    user_settings = util.read_user_settings()
    
    user_id_1 = user_settings["user_id_1"]
    user_id_2 = user_settings["user_id_2"]
    user_id_3 = user_settings["user_id_3"]

    ids = [user_id_1, user_id_2, user_id_3]

    group_size = 3 if user_id_3 != "" else 2

    # Open you default camera
    cap = cv.VideoCapture(0)
    cap.set(cv.CAP_PROP_BUFFERSIZE, 1)
    er = PyEmotion.DetectFace(device='cpu', gpu_id=0)
    firebase.init_firebase()
    while True:
        _, frame = cap.read()
        _, emotions = er.predict_emotion(frame)
        _set_state_from_emotion(emotions, group_size, ids)
        # only find emotion once every second
        time.sleep(1)

def _set_state_from_emotion(new_emotions, group_size, ids):
    """ Set the new emotion to True and the rest to False. """
    if (new_emotions) == "noface": # no face detected
         return
    
    if len(new_emotions) > 1: # several faces detected

        for i in range(group_size):
            if i >= len(new_emotions): break # if we have more ids than faces detected
            emotion = new_emotions[i].lower()
            emotion_dict = _compute_emotions_dict(emotion)
            firebase.add_data(ids[i], emotion_dict)
            _write_emotions_to_csv(emotion_dict, ids[i])
    
    else: # only one face detected. assume this is the left person
        # maybe we should ignore this case, because we don't know which person it is
        emotion = new_emotions[0].lower()
        emotion_dict = _compute_emotions_dict(emotion)
        firebase.add_data(ids[0], emotion_dict)
        _write_emotions_to_csv(emotion_dict, ids[0]) # defaults to the first id
        
def _compute_emotions_dict(current_emotion):
    emotions = DEFAULT_EMOTIONS
    for e in emotions.keys():
        emotions[e] = False
    emotions[current_emotion] = True
    return emotions

def _write_emotions_to_csv(emotions, id):
        filepath = f'data/emotions_{id}.csv'
        file_exists = os.path.exists(filepath) and os.path.getsize(filepath) > 0
        timestamp = time.time()
        emotions_with_timestamp = {"timestamp": timestamp}
        emotions_with_timestamp.update(emotions)

        with open(filepath, 'a', newline='') as csvfile:
            fieldnames = ['timestamp'] + list(DEFAULT_EMOTIONS.keys())
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

            # Write the header only if the file did not exist or was empty
            if not file_exists:
                writer.writeheader()

            # Write the updated emotions as a new row
            writer.writerow(emotions_with_timestamp)
