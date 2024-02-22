from django.shortcuts import render

import random
import csv
from rest_framework.decorators import api_view
from rest_framework.response import Response
from dataprocessing.measurements.engagement import compute_engagement
from dataprocessing.states import MeasurementStates

from dataprocessing.services import append_clickstream, fetch_and_process_number, get_newest_clickstream_setence
from dataprocessing.util import read_from_csv
from .serializers import StateSerializer

"""
This file is responsible for the endpoints, that means handling the requests and responses of the API.
"""

@api_view(['GET'])
def hello_world(request):
    return Response({'message': 'Hello from Django'})

@api_view(['GET'])
def number(request):
    number = fetch_and_process_number()
    return Response({'number': number})

STATES = ['neutral', 'angry', 'fear', 'happy', 'sad', 'surprise', 'disgust', 'engagement', 'stress']
IDS = range(1, 11)

# Initialize with a default state for each ID
random_states = [{'id': id, 'state': random.choice(STATES)} for id in IDS]

@api_view(['GET'])
def state_view(request):
    # Select a random ID
    random_id = random.choice(IDS)
    # Update the state of the selected ID
    for state in random_states:
        if state['id'] == random_id:
            state['state'] = random.choice(STATES)
            break
    
    serializer = StateSerializer(random_states, many=True)
    return Response(serializer.data)

@api_view(['GET', 'POST'])
def add_clickstream(request):
    if request.method == 'POST':
        append_clickstream(request.data)
        return Response({'status': 'success'})
    
    data = get_newest_clickstream_setence()
    return Response({'sentence': data})

@api_view(['GET'])
def get_computed_engagement(request):
    t, f, d = read_from_csv('data/EDA.csv')
    amplitude, nr_peaks, auc = compute_engagement(d)
    print(f"Amplitude: {amplitude}")
    print(f"Number of peaks: {nr_peaks}")
    print(f"Area under curve: {auc}")
    return Response({'amplitude': amplitude, 'nr_peaks': nr_peaks, 'auc': auc})

# Endre noe på denne?
@api_view(['GET'])
def get_real_state(request):
    filepath = 'data/states.csv'  # Path to your CSV file
    try:
        # Initialize an empty dictionary to hold the last row data
        last_row_data = {}
        # Open the CSV file and read the last row
        with open(filepath, 'r', newline='') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                last_row_data = row  # This will end up being the last row
        
        # Check if last_row_data is still empty, which means the file was empty
        if not last_row_data:
            return Response({"error": "No data found in CSV file."}, status=404)
        
        # Convert values from strings to appropriate types (boolean in this case)
        for key in last_row_data:
            last_row_data[key] = True if last_row_data[key].lower() == 'true' else False
        
        return Response(last_row_data)
    except FileNotFoundError:
        return Response({"error": "CSV file not found."}, status=404)
    except Exception as e:
        # Generic error handling
        return Response({"error": str(e)}, status=500)