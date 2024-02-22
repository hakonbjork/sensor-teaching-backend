from collections import deque

import numpy as np
import datetime

from dataprocessing import util, states

class DataHandler:
    """
    Class that subscribes to a specific raw data stream,
    handles storing the data,
    preprocessing the data,
    and calculating measurements from the data
    """
    def __init__(self, measurement_func=None, measurement_path=None, measurement_type=None,
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
        self.window_step = window_step
        self.window_length = window_length
        self.measurement_func = measurement_func
        self.measurement_path = measurement_path
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
            normalized_measurement = np.dot(measurement, np.reciprocal(self.baseline)) / len(self.baseline)
            # print(f"measurement: {measurement}, normalized_measurement: {normalized_measurement}, path: {self.measurement_path}")
            # could be useful to do this, or maybe json
            # finne ut hvordan sende til frontend, midlertidig lagring her kan være bare å ha til en liste over hva alle statesene er
            # det som må lagres over tid skal uansett gjøre det på en eller annen måte
            # evt csv som de gjør her da men tror ikke vi trenger så "mye" lagring

            # print(f"measurement: {measurement}, path: {self.measurement_path}, normalized_measurement: {normalized_measurement}")
            print(f"{self.measurement_type}: {normalized_measurement}")
            # states.states[self.measurement_type] = normalized_measurement

            if (self.measurement_type == "engagement" or self.measurement_type == "stress"): # and normalized_measurement > 1.25:
                states.MeasurementStates.set_state_from_normalized_measurement(self.measurement_type, normalized_measurement)
            
            # if len(measurement) == 1:
            #     util.write_csv(self.measurement_path, [normalized_measurement])
            # else:
            #     util.write_csv(self.measurement_path,
            #                    [normalized_measurement, *measurement],
            #                    header_features=self.header_features)
