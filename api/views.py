from django.shortcuts import render

from rest_framework.decorators import api_view
from rest_framework.response import Response

from dataprocessing.services import fetch_and_process_number
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
    data = [{'id': 1, 'state': 'flow'},
            {'id': 2, 'state': 'stressed'},
            {'id': 3, 'state': 'disengaged'},
            {'id': 4, 'state': 'flow'},
            {'id': 5, 'state': 'sensor issues'}]
    
    serializer = StateSerializer(data, many=True)
    return Response(serializer.data)