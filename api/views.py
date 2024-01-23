from django.shortcuts import render

import random
from rest_framework.decorators import api_view
from rest_framework.response import Response

from dataprocessing.services import append_clickstream, fetch_and_process_number, get_newest_clickstream_setence
from .serializers import StateSerializer

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
