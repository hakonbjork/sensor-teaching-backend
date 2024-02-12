import numpy as np


def compute_percentage_of_ibi_that_differ(ibi):
    """
    Helper for emotional regulation
    :param ibi: list of ibi values
    :type ibi: list of float
    :return: percentage of ibi successive ibi values that differs by more than 50ms
    :rtype: float
    """
    assert type(ibi) == list
    assert len(ibi) > 2
    differs_more = 0
    differs_less = 0
    for i in range(1, len(ibi)):
        if abs(ibi[i] - ibi[i - 1]) > 0.05:
            differs_more += 1
        else:
            differs_less += 1
    return max(differs_more / (differs_more + differs_less), 0.01)


def compute_rmssd(ibi):
    """
    Helper for emotional regulation
    One way to measure heart rate variability.
    :param ibi: list of ibi values
    :type ibi: list of float
    :return: root mean square of successive differences
    :rtype: float
    """
    assert list == type(ibi)
    assert len(ibi) > 2
    total = 0
    for i in range(1, len(ibi)):
        total += (ibi[i] - ibi[i - 1]) ** 2
    return (total / (len(ibi) - 1)) ** 0.5


def compute_normal_ibi(ibi):
    """
    Helper for emotional regulation
    Removes IBI values that are below the 10th percentile and above the 90th percentile.
    :param ibi: list of ibi values
    :type ibi: list of float
    :return: a list of ibi values where the 10th and 90th percentile are removed
    :rtype: list of float
    """

    min_ibi = np.percentile(np.asarray(ibi), 10)
    max_ibi = np.percentile(np.asarray(ibi), 90)
    return [value for value in ibi if min_ibi < value < max_ibi]


def compute_emotional_regulation(ibi):
    """
    Computes emotional regulation based on a list of IBI values
    :param ibi: list of ibi values
    :type ibi: list of float
    :return: a measure of emotional regulation
    :rtype: float, float, float
    """
    rmssd = compute_rmssd(ibi)
    percentage_that_differ = compute_percentage_of_ibi_that_differ(ibi)
    normal = compute_normal_ibi(ibi)
    return rmssd, percentage_that_differ, np.average(normal)
