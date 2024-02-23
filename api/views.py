from django.shortcuts import render

import random
from rest_framework.decorators import api_view
from rest_framework.response import Response

from dataprocessing.services import append_clickstream, get_newest_clickstream_setence
from dataprocessing.util import read_last_row_of_csv
from .serializers import StateSerializer

"""
This file is responsible for the endpoints, that means handling the requests and responses of the API.
"""

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
def get_real_state(request):
    """ Combines the data from the three measurements (csv's) and returns it as a dictionary."""

    # fiks caset at filene ikke eksisterer

    all_data = {}
    stress_dict = read_last_row_of_csv('data/stress.csv')
    engagement_dict = read_last_row_of_csv('data/engagement.csv')
    emotions_dict = read_last_row_of_csv('data/emotions.csv')

    # må mulig endre hvordan det er hvis vi ikke har måling,
    # men per nå settes det bare til False

    if stress_dict is None:
        stress_dict = {'stress': False}

    if engagement_dict is None:
        engagement_dict = {'engagement': False}
    
    if emotions_dict is None:
        emotions_dict = {'angry': False, 'fear': False, 'happy': False, 'sad': False, 'surprise': False, 'disgust': False}

    all_data.update(stress_dict)
    all_data.update(engagement_dict)
    all_data.update(emotions_dict)

    return Response(all_data)
