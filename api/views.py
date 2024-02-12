from django.shortcuts import render

import random
from rest_framework.decorators import api_view
from rest_framework.response import Response
from dataprocessing.measurements.engagement import compute_engagement

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

STATES = ['flow', 'stressed', 'disengaged', 'sensor issues']
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
