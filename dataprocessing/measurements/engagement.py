import numpy as np

""" This file is responsible for the computation of the engagement features. """

""" Constants """
FQ = 4  # frequency of data points, 4 per seconds
MEAN_KERNEL_WIDTH = 5 * FQ  # The width (data points) of the mean kernel
ONSET_THRESHOLD = 0.01  # the threshold in microsiemens required to classify an onset of a peak
OFFSET_THRESHOLD = 0  # the threshold in microsiemens required to classify an offset of a peak


def compute_engagement(eda):
    """
    Compute three different features correlated with engagement

    :param eda: list of eda data points
    :type eda: list of float
    :return: amplitude, number of peaks of phasic signal, and area under the curve of tonic signal
    :rtype: (float, float, float)
    """

    # find tonic and phasic components
    mean_arr = _mean_filter(eda)
    relevant_eda = eda[MEAN_KERNEL_WIDTH: -MEAN_KERNEL_WIDTH]
    tonic = mean_arr - abs(min(relevant_eda - mean_arr))
    phasic = relevant_eda - tonic

    # features
    peak_start, peak_end = _find_peaks(relevant_eda - mean_arr)
    amplitude = _find_amplitude(peak_start, peak_end, phasic)
    nr_peaks = sum(peak_start)
    auc = _area_under_curve(tonic)

    return amplitude, nr_peaks, auc


def _mean_filter(eda):
    """
    Compute the mean eda signal, using a mean kernel of 10 seconds width

    :param eda: list of eda data points
    :type eda: list of float
    :return: mean filter of the signal
    :rtype: np.array
    """
    mean_arr = np.array([])
    for i in range(MEAN_KERNEL_WIDTH, len(eda) - MEAN_KERNEL_WIDTH):
        mean = np.mean(eda[i - MEAN_KERNEL_WIDTH: i + MEAN_KERNEL_WIDTH + 1])
        mean_arr = np.append(mean_arr, mean)
    return mean_arr


def _find_peaks(modified_phasic):
    """
    Find the position of peak start and peak ends on the phasic signal

    :param modified_phasic: list of the phasic signal data points
    :type modified_phasic: list of float
    :return: two lists with 1 where peaks starts and ends respectively
    :rtype: (list of int, list of int)
    """
    peak_start = np.zeros(len(modified_phasic))
    peak_end = np.zeros(len(modified_phasic))
    rising = False

    # identify if start is peak
    if ONSET_THRESHOLD < modified_phasic[0] < modified_phasic[1]:
        peak_start[0] = 1
        rising = True

    for i in range(len(modified_phasic) - 1):
        # peak starts from the point it gets above the onset threshold
        if modified_phasic[i] < ONSET_THRESHOLD < modified_phasic[i + 1] and not rising:
            peak_start[i + 1] = 1
            rising = True
        # peak ends from the point it dips below the offset threshold
        elif modified_phasic[i] > OFFSET_THRESHOLD > modified_phasic[i + 1] and rising:
            peak_end[i + 1] = 1
            rising = False

    return peak_start, peak_end


def _find_amplitude(peak_start, peak_end, phasic):
    """
    Find the total amplitude of the highest points of each peak

    :param peak_start: where the peaks in the phasic signal starts
    :type peak_start: list of int
    :param peak_end: where the peaks in the phasic signal ends
    :type peak_end: list of int
    :param phasic: list of the phasic signal data points
    :type phasic: list of float
    :return: the amplitude of the phasic signal
    :rtype: float
    """
    amplitude = 0
    for i in range(len(phasic)):
        # if we found a peak start
        if peak_start[i] == 1:
            j = i
            # find the peak end (or end of data points)
            while j < len(phasic) and peak_end[j] != 1:
                j += 1
            # find the highest point of phasic in the range from the start of peak to end of peak
            amplitude += max(phasic[i:j + 1])

    return amplitude


def _area_under_curve(tonic):
    """
    Computes the area under the curve of the tonic signal, using trigonometry

    :param tonic: list of the tonic signal
    :type tonic: list of float
    :return: area under the curve of the tonic signal
    :rtype: float
    """
    auc = 0
    for i in range(len(tonic) - 1):
        # first data point
        y1 = tonic[i]
        # second datapoint
        y2 = tonic[i + 1]
        # change in y
        dy = y2 - y1
        # change in x
        dx = 1 / FQ

        area_square = y1 * dx
        area_triangle = dy * dx / 2
        auc += area_square + area_triangle

    return auc
