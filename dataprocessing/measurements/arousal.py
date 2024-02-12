def compute_arousal(eda):
    """
    calculating arousal based on EDA positive change [1]

    Goes through every data point in a window, sum up all positive changes from subsequent data points

    [1] Leiner, D. J., Fahr, A., & Früh, H. (2012). EDA Positive Change: A Simple Algorithm for
    Electrodermal Activity to Measure General Audience Arousal During Media Exposure.
    Communication Methods and Measures, 6 (4), 237–250.

    :param eda: list of eda data points
    :type eda: list of float
    :return: positive_change - a measure for arousal
    :rtype: list of float
    """
    positive_change = 0
    for i in range(len(eda) - 1):
        if eda[i + 1] > eda[i]:
            positive_change += eda[i + 1] - eda[i]

    return float(positive_change)
