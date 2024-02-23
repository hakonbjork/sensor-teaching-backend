import csv
from .measurements.engagement import compute_engagement

def to_list(x):
    """ make a list out of x if it is not already a list"""
    if isinstance(x, list):
        return x
    try:
        return list(x)
    except TypeError:
        return [x]
    
def read_last_row_of_csv(filepath):
    """ Read the last row of a CSV file and return it as a dictionary.
    Expects the first row to be the header row, the first value to be timestamp and the rest to be boolean values."""
    # Initialize an empty dictionary to hold the last row data
    last_row_data = {}
    try:
        # Open the CSV file and read the last row
        with open(filepath, 'r', newline='') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                last_row_data = row  # This will end up being the last row
        
        # Check if last_row_data is still empty, which means the file was empty
        if not last_row_data:
            return None
        
        # Convert values from strings to appropriate types (boolean in this case)
        for key in last_row_data:
            if key != 'timestamp':
                last_row_data[key] = True if last_row_data[key].lower() == 'true' else False
        
        # remove the timestamp value
        if 'timestamp' in last_row_data:  
            del last_row_data['timestamp']

        return last_row_data
    except FileNotFoundError:
        return None