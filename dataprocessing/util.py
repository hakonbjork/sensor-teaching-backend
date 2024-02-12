import csv
from .measurements.engagement import compute_engagement

def read_from_csv(csv_file):
    """
    Read data from a csv file.

    :param csv_file: path to the csv file
    :return: a list of containing of the first column of the file
    """
    with open(csv_file, 'r') as file:
        reader = csv.reader(file)
        data = [float(row[0]) for row in reader]
        timestamp = int(data.pop(0))
        framerate = int(data.pop(0))

    return timestamp, framerate, data

def test_read_from_csv():
    """ Test function to test the read_from_csv function """
    t, f, d = read_from_csv('../data/EDA.csv')
    print(f"Unix timestamp: {t}")
    print(f"Framerate: {f}")
    print(f"First 10 numbers of list: {d[:10]}")

def test_compute_engagement():
    """ Test function to test the compute_engagement function """
    t, f, d = read_from_csv('data/EDA.csv')
    amplitude, nr_peaks, auc = compute_engagement(d)
    print(f"Amplitude: {amplitude}")
    print(f"Number of peaks: {nr_peaks}")
    print(f"Area under curve: {auc}")

def to_list(x):
    """ make a list out of x if it is not already a list"""
    if isinstance(x, list):
        return x
    try:
        return list(x)
    except TypeError:
        return [x]
