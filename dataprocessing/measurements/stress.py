import numpy as np


def compute_stress(temps_list):
    """
    Predicts acute stress based on GSR temperature
    :param temps_list: list of temperatures
    :return: returns the overall change in temperature in the list
    """
    slope = np.polyfit([0.25 * i for i in range(len(temps_list))], temps_list, 1)[0]
    negative_slope = np.negative(slope)
    return float(negative_slope)
