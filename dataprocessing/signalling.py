import time
from . import firebase
import numpy as np

def compute_signalling(user_id, start_time):
    """ This function will compute signalling based on the firebase data.
     For the chosen user_id, it will fetch all the data from the last 5 minutes,
     and compute the signalling based on the data. The signalling will be sent to firebase,
     for now only as booleans based on the values calculated in this function."""
    
    EMOTION_FRACTION_THRESHOLD = 0.35
    HAPPY_FRACTION_THRESHOLD = 0.08

    # might also use csv files here
    user_data = firebase.get_user_data(user_id)
    if (user_data == None): # If no data for the user is found, try again later. Will be the case at the start
        print(f"Compute signalling: no user data found for user {user_id}, trying again in 5 seconds...")
        time.sleep(5)
        new_start_time = time.time()
        return compute_signalling(user_id, new_start_time)
    
    measurements = ["stress", "engagement", "surprise", "fear", "happy", "sad", "angry", "disgust"]
    # can ignore noface and neutral here,
    # since we don't care if a person has been neutral the last x minutes

    current_time = time.time()
    five_minutes_ago = current_time - 300 # this can be changed based on how long we want to look back

    # if five minutes have not passed, figure out how many seconds have passed and use start_time
    elapsed_seconds = current_time - start_time
    is_over_five_minutes = elapsed_seconds > 300
    five_min_ago_or_start_time  = five_minutes_ago if is_over_five_minutes else start_time

    # for testing, since there might not be data available last 5 minutes
    mock_time = 1709730200
    mock_current_time = mock_time + 2800 # random value, capture a lot of data

    # calculate the total number of emotion entries in the last 5 minutes
    # to later find the fraction of for example sad entries
    emotion_entries_last_five_min = 0
    sad_entries_last_five_min = 0
    emotions = ["happy", "sad", "angry", "disgust", "fear", "surprise", "noface", "neutral"]
    for emotion in emotions:
        if (not emotion in user_data):
            continue
        emotion_data = user_data[emotion]
        emotion_entries = sum(1 for item in emotion_data.values() if item != "" and item['time'] > five_min_ago_or_start_time and item['value'] >= 1)
        emotion_entries_last_five_min += emotion_entries
        if (emotion == "sad"): sad_entries_last_five_min += emotion_entries

    for measurement in measurements:
        if (not measurement in user_data):
            # print(f"did not found {measurement} in user data for user {user_id}")
            continue # if for example no disgust data

        data = user_data[measurement] # data for the current measurement

        if (measurement == "stress" or measurement == "engagement"):
            # the stress and engagement from empatica
            # this calculation will find the mean and the standard deviation from all time,
            # and then look at the current window (last minute) to see if the mean value is significantly different

            all_values = [item for item in data.values() if item != ""]
            std_deviation = float(np.std([item['value'] for item in all_values]))
            mean_value = float(np.mean([item['value'] for item in all_values]))
            window_count = 0
            window_sum = 0
            one_minute_ago = current_time - 60

            for item in data.values():
                # if we have a buggy instance (instance with no data), ignore it
                # might also change other code so that we don't get these instances
                if item == "":
                    continue
                if item['time'] > one_minute_ago:
                    window_count += 1
                    window_sum += item['value']

            if (window_count == 0):
                continue

            mean_window_value = float(window_sum / window_count)

            if (measurement == "engagement"):
                signal_true = mean_window_value < mean_value - std_deviation
                firebase.update_signalling_data(user_id, measurement, signal_true)

            else: # stress
                signal_true = mean_window_value > mean_value + std_deviation
                firebase.update_signalling_data(user_id, measurement, signal_true)

        elif (measurement == "happy"):
            continue # ignore happy, should not matter if they smile too little
        
        elif (measurement == "sad"):
            timestamps = [item['time'] for item in data.values() if item != "" and item['time'] > start_time]
            if (len(timestamps) == 0): continue

            # Convert timestamps to minutes since the first timestamp
            normalized_minutes = (np.array(timestamps) - np.min(timestamps)) // 60

            # Get the unique minutes and count of events in each minute
            unique_minutes, counts_per_minute = np.unique(normalized_minutes, return_counts=True)

            # Calculate the mean and standard deviation
            mean_frequency = float(np.mean(counts_per_minute))
            std_deviation = float(np.std(counts_per_minute))

            min_since_start = (time.time() - start_time) // 60 + 1
            mean_last_five_min = sad_entries_last_five_min / min(min_since_start, 5)

            signal_true = mean_last_five_min > mean_frequency + std_deviation
            firebase.update_signalling_data(user_id, measurement, signal_true)

        # the emotions from camera, except from happy and sad
        else:
            # this calculation will look at how many emotion instances of the last 5 minutes that the user was for example sad
            # we look at the fraction of each of the emotion measurements, and signal if abow/below a certain threshold
            # here, we also have to consider that if less than 300 seconds have passed, have to calculate based on start time

            if emotion_entries_last_five_min == 0:
                continue

            count_high_values = sum(1 for item in data.values() if item != "" and item['time'] > five_min_ago_or_start_time and item['value'] >= 1)
            fraction_of_total = count_high_values / emotion_entries_last_five_min

            # print(f"user_id {user_id}: fraction of {measurement} is {fraction_of_total}")

            if (measurement == "happy"):
                signal_true = fraction_of_total < HAPPY_FRACTION_THRESHOLD # if less happy than threshold, signal true
                firebase.update_signalling_data(user_id, measurement, signal_true) 

            else:
                signal_true = fraction_of_total > EMOTION_FRACTION_THRESHOLD # for sad emotions, signal if more than threshold
                firebase.update_signalling_data(user_id, measurement, signal_true) 

def start_computing_signalling(user_id):
    firebase.init_firebase()
    start_time = time.time()
    while True:
        compute_signalling(user_id, start_time)
        time.sleep(5) # for now, updates signalling every 5. second
