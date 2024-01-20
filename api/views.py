from django.shortcuts import render

from rest_framework.decorators import api_view
from rest_framework.response import Response

from dataprocessing.services import fetch_and_process_number

@api_view(['GET'])
def hello_world(request):
    return Response({'message': 'Hello, world!'})

@api_view(['GET'])
def number(request):
    number = fetch_and_process_number()
    return Response({'number': number})