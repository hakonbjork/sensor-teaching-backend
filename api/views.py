from django.shortcuts import render

from random import choice
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

@api_view(['GET'])
def state_view(request):
    STATES = ['flow', 'stressed', 'disengaged', 'sensor issues']
    IDS = range(1, 11)
    random_states = [{'id': id, 'state': choice(STATES)} for id in IDS]
    
    serializer = StateSerializer(random_states, many=True)
    return Response(serializer.data)

@api_view(['GET', 'POST'])
def add_clickstream(request):
    if request.method == 'POST':
        append_clickstream(request.data)
        return Response({'status': 'success'})
    
    data = get_newest_clickstream_setence()
    return Response({'sentence': data})
