from collections import deque

import numpy as np
import os
import csv
import time
import warnings

from dataprocessing import firebase, util

warnings.filterwarnings("error", category=RuntimeWarning) # to be able to catch the divide by zero warning
class DataHandler:
    """
    Class that subscribes to a specific raw data stream,
    handles storing the data,
    preprocessing the data,
    and calculating measurements from the data
    """
    def __init__(self, id, measurement_func=None, measurement_path=None, measurement_type=None,
                 window_length=None, window_step=None,
                 baseline_length=None, header_features=[]):
        """
        :param measurement_func: the function we call to compute measurements from the raw data
        :type measurement_func: (list) -> any
        :param measurement_path: path to the output csv file
        :type measurement_path: str
        :param window_length: length of the window, i.e number of data points for the function
        :type window_length: int
        :param window_step: how many steps for a new window, i.e for 6 steps,
        a new measurement is computed every 6 data points
        :type window_step: int
        :param baseline_length: Amount of data points required to calculate baseline
        :type baseline_length: int
        """
        assert window_length and window_step and measurement_func and baseline_length, \
            "Need to supply the required parameters"

        self.data_queue = deque(maxlen=window_length)
        self.data_counter = 0
        self.id = id
        self.window_step = window_step
        self.window_length = window_length
        self.measurement_func = measurement_func
        self.measurement_type = measurement_type
        self.baseline_length = baseline_length
        self.baseline = None
        self.header_features = header_features
        self._handle_datapoint = self._calculate_baseline

    def add_data_point(self, datapoint):
        """ Receive a new data point, and call appropriate measurement function when we have enough points """
        self.data_queue.append(datapoint)
        self.data_counter += 1
        self._handle_datapoint()

    def _calculate_baseline(self):
        """ Calculates a baseline if we have received enough data points """
        if self.data_counter % self.window_step == 0 and len(self.data_queue) == self.window_length:
            measurement = util.to_list(self.measurement_func(list(self.data_queue)))
            if self.baseline is None:
                self.baseline = [[feature] for feature in measurement]
            else:
                for baseline_feature, feature in zip(self.baseline, measurement):
                    baseline_feature.append(feature)
        if self.data_counter >= self.baseline_length:
            self.baseline = [abs(sum(feature)) / len(feature) for feature in self.baseline]
            self._handle_datapoint = self._calculate_measurement

    def _calculate_measurement(self):
        """ Calculates a measurement and writes to csv if we have received enough data points """
        if self.data_counter % self.window_step == 0 and len(self.data_queue) == self.window_length:
            measurement = util.to_list(self.measurement_func(list(self.data_queue)))
            try:
                normalized_measurement = np.dot(measurement, np.reciprocal(self.baseline)) / len(self.baseline)
                if (self.measurement_type == "engagement" or self.measurement_type == "stress"):
                    self._set_state_from_normalized_measurement(normalized_measurement)
            except RuntimeWarning as w: # If we get a Runtime warning (divide by zero), we just skip the measurement
                print(f"Warning/Error calculating normalized measurement for {self.measurement_type} for user {self.id} {w}, returning")
                return
            
            # if len(measurement) == 1:
            #     util.write_csv(self.measurement_path, [normalized_measurement])
            # else:
            #     util.write_csv(self.measurement_path,
            #                    [normalized_measurement, *measurement],
            #                    header_features=self.header_features)

    def _set_state_from_normalized_measurement(self, nm):
        """ Set the state of the measurement based on the normalized measurement.
         If the normalized measurement is above a certain threshold, the state is set to True, else False. 
         This function will write either engagement, or stress, to its respective csv file.
         We use two files because a student can be both enagaged and stressed at the same time."""
        
        SWITCH_POINT = 1
        is_state_high = float(nm) > SWITCH_POINT
        firebase.add_measurement_data(self.id, self.measurement_type, float(nm))
        # self._write_measurement_to_csv(is_state_high)

    def _write_measurement_to_csv(self, is_state_high):
        filepath = "data/" + self.measurement_type + "_" + self.id + ".csv"
        file_exists = os.path.exists(filepath) and os.path.getsize(filepath) > 0

        with open(filepath, 'a', newline='') as csvfile:
            writer = csv.writer(csvfile)

            # Write the header only if the file did not exist or was empty
            if not file_exists:
                header = ["timestamp", self.measurement_type]
                writer.writerow(header)

            # Write the updated states as a new row
            formated_is_state_high = util.to_list(is_state_high)
            writer.writerow([time.time()] + formated_is_state_high)
